from flask import Flask, request, render_template, redirect, url_for, send_file, jsonify
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

from extractor import extract_text_from_pdf, parse_resume_with_llm, generate_feedback, generate_template, analyze_skill_gaps
from matcher import calculate_semantic_match, benchmark_score
from export import export_to_csv, export_to_pdf
from validators import validate_upload
from grammar_checker import check_grammar_with_gemma

# Load environment variables
load_dotenv()

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
        return render_template('analyze.html')

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
            return render_template('analyze.html', error=validation_msg)

        raw_text = extract_text_from_pdf(file_path)
        if "Error" in raw_text:
            return render_template('analyze.html', error=raw_text)

        extracted_entities = parse_resume_with_llm(raw_text)
        ats_score = calculate_semantic_match(raw_text, job_description)
        benchmark_data = benchmark_score(ats_score)
        feedback_data = generate_feedback(raw_text, job_description)
        skill_gaps = analyze_skill_gaps(raw_text, job_description)
        grammar_check = check_grammar_with_gemma(raw_text)

        return render_template('analyze.html', 
                               score=f"{ats_score}%", 
                               data=extracted_entities,
                               feedback=feedback_data.get("improvements", []),
                               job_desc=job_description,
                               rating=benchmark_data.get("rating"),
                               percentile=benchmark_data.get("percentile"),
                               industry_avg=benchmark_data.get("industry_average"),
                               comparison=benchmark_data.get("comparison"),
                               skill_gaps=skill_gaps,
                               grammar_check=grammar_check)

    except Exception as e:
        return render_template('analyze.html', error=f"An error occurred: {str(e)}")

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

@app.route('/template', methods=['GET', 'POST'])
def template_generation():
    """Generate resume template based on job description."""
    if request.method == 'GET':
        return render_template('template.html', summary='', sections=[], bullets=[])
    
    if 'job_description' not in request.form:
        return render_template('template.html', error="Please provide a job description.", summary='', sections=[], bullets=[])
    
    job_description = request.form['job_description']
    template_data = generate_template(job_description)
    
    return render_template('template.html', 
                           summary=template_data.get("summary", ""),
                           sections=template_data.get("key_sections", []),
                           bullets=template_data.get("suggested_bullets", []))

@app.route('/skill-gaps', methods=['POST'])
def skill_gaps_api():
    """API endpoint for skill gap analysis."""
    if 'resume' not in request.files or 'job_description' not in request.form:
        return jsonify({"error": "Missing resume or job description"}), 400
    
    resume_file = request.files['resume']
    job_description = request.form['job_description']
    
    filename = secure_filename(resume_file.filename)
    file_path = os.path.join(UPLOAD_DIR, filename)
    resume_file.save(file_path)
    
    raw_text = extract_text_from_pdf(file_path)
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

if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    debug_mode = os.getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)