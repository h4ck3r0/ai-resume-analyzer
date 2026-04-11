from flask import Flask, request, render_template, redirect, url_for, send_file, jsonify
import os
from werkzeug.utils import secure_filename

from extractor import extract_resume_text, parse_resume_with_llm, generate_feedback, generate_template, analyze_skill_gaps
from matcher import calculate_semantic_match, benchmark_score
from export import export_to_csv, export_to_pdf, export_template_to_csv, export_template_to_pdf
from validators import validate_upload
from grammar_checker import check_grammar_with_gemma
from analyzer_details import (extract_education, extract_work_experience, extract_contact_info,
                              analyze_ats_compliance, analyze_keyword_match, analyze_action_verbs,
                              analyze_quantification, analyze_length_and_format)

app = Flask(__name__)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.route('/')
def home():
    """Renders the Home / Landing Page."""
    return render_template('index.html')

@app.route('/about')
def about():
    """Renders the About Page."""
    return render_template('about.html')

@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    """Handles the actual Resume Analyzer tool."""
    if request.method == 'GET':
        return render_template('analyze.html', data={})

    if 'resume' not in request.files or 'job_description' not in request.form:
        return render_template('analyze.html', error="Missing file or job description.")

    resume_file = request.files['resume']
    job_description = request.form['job_description']

    filename = secure_filename(resume_file.filename)
    file_path = os.path.join(UPLOAD_DIR, filename)
    resume_file.save(file_path)

    try:
        is_valid, validation_msg = validate_upload(resume_file.filename, file_path)
        if not is_valid:
            return render_template('analyze.html', error=validation_msg, data={})

        raw_text = extract_resume_text(file_path)
        if "Error" in raw_text:
            return render_template('analyze.html', error=raw_text, data={})

        extracted_entities = parse_resume_with_llm(raw_text)
        ats_score = calculate_semantic_match(raw_text, job_description)
        benchmark_data = benchmark_score(ats_score)
        feedback_data = generate_feedback(raw_text, job_description)
        skill_gaps = analyze_skill_gaps(raw_text, job_description)
        grammar_check = check_grammar_with_gemma(raw_text)

        normalized_data = {
            'name': extracted_entities.get('Name'),
            'email': extracted_entities.get('Email'),
            'skills': extracted_entities.get('Skills') or [],
            'years_of_experience': extracted_entities.get('Total_Years_Experience') or 0
        }

        education = extract_education(raw_text)
        work_experience = extract_work_experience(raw_text)
        contact_info = extract_contact_info(raw_text)
        ats_compliance = analyze_ats_compliance(raw_text)
        matched_keywords = analyze_keyword_match(raw_text, job_description)
        action_verbs = analyze_action_verbs(raw_text)
        quantification = analyze_quantification(raw_text)
        length_format = analyze_length_and_format(raw_text)

        return render_template('analyze.html', 
                               score=f"{ats_score:.2f}%", 
                               data=normalized_data,
                               feedback=feedback_data.get("improvements", []),
                               job_desc=job_description,
                               rating=benchmark_data.get("rating"),
                               percentile=benchmark_data.get("percentile"),
                               industry_avg=benchmark_data.get("industry_average"),
                               comparison=benchmark_data.get("comparison"),
                               skill_gaps=skill_gaps,
                               grammar_check=grammar_check,
                               education=education,
                               work_experience=work_experience,
                               contact_info=contact_info,
                               ats_compliance=ats_compliance,
                               matched_keywords=matched_keywords,
                               action_verbs=action_verbs,
                               quantification=quantification,
                               length_format=length_format)

    except Exception as e:
        return render_template('analyze.html', error=f"An error occurred: {str(e)}", data={})

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

@app.route('/template', methods=['GET', 'POST'])
def template_generation():
    """Generate resume template based on job description."""
    if request.method == 'GET':
        return render_template('template.html', summary='', sections=[], bullets=[], recommended_skills=[], cover_letter='', career_level='Mid-Level')
    
    if 'job_description' not in request.form:
        return render_template('template.html', error="Please provide a job description.", summary='', sections=[], bullets=[], recommended_skills=[], cover_letter='')
    
    job_description = request.form['job_description']
    career_level = request.form.get('career_level', 'Mid-Level')
    template_data = generate_template(job_description)
    
    recommended_skills = extract_keywords_from_job(job_description)
    
    cover_letter = generate_cover_letter_opening(job_description, career_level)
    
    return render_template('template.html', 
                           summary=template_data.get("summary", ""),
                           sections=template_data.get("key_sections", []),
                           bullets=template_data.get("suggested_bullets", []),
                           recommended_skills=recommended_skills,
                           cover_letter=cover_letter,
                           career_level=career_level,
                           job_description=job_description)

@app.route('/skill-gaps', methods=['POST'])
def skill_gaps_api():
    if 'resume' not in request.files or 'job_description' not in request.form:
        return jsonify({"error": "Missing resume or job description"}), 400
    
    resume_file = request.files['resume']
    job_description = request.form['job_description']
    
    filename = secure_filename(resume_file.filename)
    file_path = os.path.join(UPLOAD_DIR, filename)
    resume_file.save(file_path)
    
    raw_text = extract_resume_text(file_path)
    skill_gaps = analyze_skill_gaps(raw_text, job_description)
    
    if os.path.exists(file_path):
        os.remove(file_path)
    
    return jsonify(skill_gaps)

@app.route('/export/<format>', methods=['POST'])
def export_analysis(format):
    """Export analysis results in CSV or PDF format."""
    from io import BytesIO
    
    analysis_data = request.json
    
    try:
        if format == 'csv':
            csv_content = export_to_csv(analysis_data)
            return send_file(
                BytesIO(csv_content.encode('utf-8')),
                as_attachment=True,
                download_name='resume_analysis.csv',
                mimetype='text/csv'
            )
        
        elif format == 'pdf':
            pdf_bytes = export_to_pdf(analysis_data)
            return send_file(
                BytesIO(pdf_bytes),
                as_attachment=True,
                download_name='resume_analysis.pdf',
                mimetype='application/pdf'
            )
        else:
            return jsonify({"error": "Invalid format"}), 400
    except Exception as e:
        return jsonify({"error": f"Export failed: {str(e)}"}), 500

@app.route('/export-template/<format>', methods=['POST'])
def export_template(format):
    """Export template in CSV or PDF format."""
    from io import BytesIO
    from datetime import datetime
    
    try:
        template_data = request.json
        template_data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if format == 'csv':
            csv_content = export_template_to_csv(template_data)
            return send_file(
                BytesIO(csv_content.encode('utf-8')),
                as_attachment=True,
                download_name='resume_template.csv',
                mimetype='text/csv'
            )
        
        elif format == 'pdf':
            pdf_bytes = export_template_to_pdf(template_data)
            return send_file(
                BytesIO(pdf_bytes),
                as_attachment=True,
                download_name='resume_template.pdf',
                mimetype='application/pdf'
            )
        
        elif format == 'txt':
            txt_content = format_template_as_text(template_data)
            return send_file(
                BytesIO(txt_content.encode('utf-8')),
                as_attachment=True,
                download_name='resume_template.txt',
                mimetype='text/plain'
            )
        else:
            return jsonify({"error": "Invalid format"}), 400
    except Exception as e:
        return jsonify({"error": f"Export failed: {str(e)}"}), 500

def extract_keywords_from_job(job_description: str) -> list:
    keywords = []
    job_desc_lower = job_description.lower()
    
    common_skills = [
        'Python', 'JavaScript', 'Java', 'C++', 'C#', 'PHP', 'Ruby', 'Go', 'Rust', 'TypeScript',
        'React', 'Vue', 'Angular', 'Node.js', 'Django', 'Flask', 'FastAPI', 'Spring Boot',
        'AWS', 'Azure', 'Google Cloud', 'Docker', 'Kubernetes', 'Git', 'Jenkins', 'CI/CD',
        'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Elasticsearch', 'SQL',
        'HTML', 'CSS', 'REST API', 'GraphQL', 'Microservices', 'Agile', 'Scrum',
        'Machine Learning', 'AI', 'TensorFlow', 'PyTorch', 'Data Analysis', 'Tableau',
        'Linux', 'Windows Server', 'Nginx', 'Apache', 'Terraform', 'Ansible'
    ]
    
    for skill in common_skills:
        if skill.lower() in job_desc_lower:
            keywords.append(skill)
    
    return keywords[:15]  # Return top 15 skills

def generate_cover_letter_opening(job_description: str, career_level: str) -> str:

    openings = {
        'Entry-Level': f"I am an enthusiastic professional eager to launch my career in this field. With a strong foundation in core competencies and eagerness to learn, I am excited to contribute to your team.",
        'Mid-Level': f"With [X years] of professional experience developing robust solutions and driving results, I am confident in my ability to make immediate contributions to your organization.",
        'Senior': f"As a seasoned professional with extensive experience in [field], I have consistently delivered strategic solutions that drive business growth and innovation.",
        'Executive': f"Throughout my career, I have successfully led cross-functional teams and implemented transformational initiatives that directly impact organizational success."
    }
    return openings.get(career_level, openings['Mid-Level'])

def format_template_as_text(template_data: dict) -> str:
    """Format template data as plain text."""
    text = "RESUME TEMPLATE\n"
    text += "=" * 80 + "\n\n"
    
    text += "PROFESSIONAL SUMMARY\n"
    text += "-" * 40 + "\n"
    text += template_data.get("summary", "") + "\n\n"
    
    text += "KEY RESUME SECTIONS\n"
    text += "-" * 40 + "\n"
    for section in template_data.get("sections", []):
        text += f"• {section}\n"
    text += "\n"
    
    text += "SUGGESTED ACHIEVEMENT BULLETS\n"
    text += "-" * 40 + "\n"
    for bullet in template_data.get("bullets", []):
        text += f"✓ {bullet}\n"
    text += "\n"
    
    text += "RECOMMENDED SKILLS\n"
    text += "-" * 40 + "\n"
    text += ", ".join(template_data.get("recommended_skills", [])) + "\n\n"
    
    text += "COVER LETTER OPENING\n"
    text += "-" * 40 + "\n"
    text += template_data.get("cover_letter", "") + "\n"
    
    return text

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)