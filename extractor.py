import pdfplumber
import json
import os
import re
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

try:
    client = genai.Client()
except Exception as e:
    pass

def _call_gemini_with_retry(prompt: str, max_retries: int = 3) -> str:
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=prompt,
                config=types.GenerateContentConfig(response_mime_type="application/json"),
            )
            return response.text
        except Exception as e:
            error_msg = str(e)
            if attempt < max_retries - 1 and ("503" in error_msg or "429" in error_msg or "UNAVAILABLE" in error_msg):
                wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                time.sleep(wait_time)
            else:
                raise e
    return None

def extract_text_from_pdf(pdf_path: str) -> str:
    text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
    except Exception as e:
        return f"Error reading PDF: {str(e)}"
    return text


def extract_text_from_docx(docx_path: str) -> str:
    """Extract text from DOCX files."""
    text = ""
    try:
        from docx import Document
        doc = Document(docx_path)
        for para in doc.paragraphs:
            if para.text.strip():
                text += para.text + "\n"
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    if cell.text.strip():
                        text += cell.text + "\n"
    except ImportError:
        return "Error: python-docx library not installed. Please install it to support DOCX files."
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"
    return text


def extract_resume_text(file_path: str) -> str:
   
    if not file_path:
        return "Error: No file path provided"
    
    file_ext = file_path.rsplit('.', 1)[-1].lower() if '.' in file_path else ''
    
    if file_ext == 'pdf':
        return extract_text_from_pdf(file_path)
    elif file_ext in ('docx', 'doc'):
        return extract_text_from_docx(file_path)
    else:
        return f"Error: Unsupported file format: .{file_ext}"

def _extract_name_from_text(text: str) -> str:
   
    if not text:
        return None
    
    lines = text.strip().split('\n')
   
    for line in lines:
        line = line.strip()
        # Skip lines that are obviously not names (too long, all caps headers, etc)
        if len(line) > 50 or line.isupper():
            continue
        # Skip lines with email or special characters
        if '@' in line or '(' in line or ')' in line:
            continue
        # First substantial line is likely the name
        if len(line) > 2 and len(line.split()) <= 4:
            return line
    return None


def _extract_email_from_text(text: str) -> str:
    """Extract email from resume text."""
    if not text:
        return None
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    return email_match.group() if email_match else None


def _extract_years_experience_from_text(text: str) -> int:
    """Extract years of experience from resume text."""
    if not text:
        return 0
    
    experience_matches = re.findall(r'(\d+)\+?\s*(?:years?|yrs?)\s+(?:of\s+)?(?:experience|exp)', text.lower())
    if experience_matches:
        # Return the maximum found (usually most relevant)
        return max(int(x) for x in experience_matches)
    
    exp_match = re.search(r'(\d+)\s+years?\s+(?:of\s+)?(?:professional\s+)?experience', text.lower())
    if exp_match:
        return int(exp_match.group(1))
    
    return 0


def parse_resume_with_llm(text: str) -> dict:
    prompt = f"""
    You are an expert technical recruiter. Extract the following information from the resume text below.
    Output ONLY a valid JSON object with the exact keys: "Name", "Email", "Skills" (list of strings), and "Total_Years_Experience" (integer).
    If any field is not found, use null for Name/Email, empty list for Skills, and 0 for Total_Years_Experience.
    
    Resume Text:
    {text}
    """
    try:
        response_text = _call_gemini_with_retry(prompt)
        if response_text:
            parsed = json.loads(response_text)
            result = {
                'Name': parsed.get('Name'),
                'Email': parsed.get('Email'),
                'Skills': parsed.get('Skills', []),
                'Total_Years_Experience': parsed.get('Total_Years_Experience', 0)
            }
            # Use fallback extraction if LLM didn't find key data
            if not result['Name']:
                result['Name'] = _extract_name_from_text(text)
            if not result['Email']:
                result['Email'] = _extract_email_from_text(text)
            if not result['Total_Years_Experience']:
                result['Total_Years_Experience'] = _extract_years_experience_from_text(text)
            return result
        else:
           
            return {
                'Name': _extract_name_from_text(text),
                'Email': _extract_email_from_text(text),
                'Skills': [],
                'Total_Years_Experience': _extract_years_experience_from_text(text)
            }
    except json.JSONDecodeError as e:
      
        return {
            'Name': _extract_name_from_text(text),
            'Email': _extract_email_from_text(text),
            'Skills': [],
            'Total_Years_Experience': _extract_years_experience_from_text(text)
        }
    except Exception as e:
        
        return {
            'Name': _extract_name_from_text(text),
            'Email': _extract_email_from_text(text),
            'Skills': [],
            'Total_Years_Experience': _extract_years_experience_from_text(text)
        }

def generate_feedback(resume_text: str, job_description: str) -> dict:
    prompt = f"""
    Act as an expert technical recruiter. Compare the candidate's resume to the job description.
    Identify the biggest gaps or missing keywords. 
    Provide specific, actionable feedback on how to improve the resume.
    Output ONLY a valid JSON object with a single key "improvements" containing a list of 5 specific improvement suggestions as strings.
    
    Format each suggestion starting with what to improve, then how to improve it.
    Example: "Add AWS certification to skills section - mention specific services used"
    
    Job Description:
    {job_description}
    
    Resume Text:
    {resume_text}
    """
    try:
        response_text = _call_gemini_with_retry(prompt)
        if response_text:
            result = json.loads(response_text)
            if "improvements" in result and isinstance(result["improvements"], list) and len(result["improvements"]) > 0:
                return result
            else:
                return {"improvements": ["Add more specific metric-driven achievements", "Highlight relevant certifications and training", "Optimize keywords for ATS systems", "Quantify your impact with numbers", "Tailor experience descriptions to job requirements"]}
        else:
            return {"improvements": ["API temporarily unavailable. Please try again in a moment."]}
    except json.JSONDecodeError:
        return {"improvements": ["Add more specific metric-driven achievements", "Highlight relevant certifications and training", "Optimize keywords for ATS systems", "Quantify your impact with numbers", "Tailor experience descriptions to job requirements"]}
    except Exception as e:
        return {"improvements": ["Add more achievement-oriented descriptions", "Include relevant technical skills", "Highlight measurable results and impact", "Use action verbs and keywords from job posting", "Format consistently for ATS compatibility"]}

def generate_template(job_description: str) -> dict:
    prompt = f"""
    Act as an expert resume writer. Based on the job description provided, generate a resume template with suggested sections and content.
    Output ONLY a valid JSON object with these EXACT keys: 
    - "summary" (2-3 sentence professional summary)
    - "key_sections" (list of 5-6 section names like "Professional Summary", "Experience", "Education", "Skills")
    - "suggested_bullets" (list of 5 achievement bullet points tailored to this role)
    
    Ensure ALL fields are non-empty lists or strings.
    
    Job Description:
    {job_description}
    """
    try:
        response_text = _call_gemini_with_retry(prompt)
        if response_text:
            result = json.loads(response_text)
            if "summary" in result and "key_sections" in result and "suggested_bullets" in result:
                if result["key_sections"] and result["suggested_bullets"]:
                    return result
        
        # Fallback with smart suggestions based on job description
        return _generate_template_fallback(job_description)
    except json.JSONDecodeError:
        return _generate_template_fallback(job_description)
    except Exception as e:
        return _generate_template_fallback(job_description)


def _generate_template_fallback(job_description: str) -> dict:
    jd_keywords = job_description.lower().split()
    

    is_senior = any(word in job_description.lower() for word in ["senior", "lead", "manager", "principal", "architect"])
    is_junior = any(word in job_description.lower() for word in ["junior", "entry", "graduate", "intern"])
    
    years_match = [w for w in jd_keywords if '+' in w and 'year' in job_description.lower()]
    
    if is_senior:
        summary = f"Results-driven professional with proven expertise in leading technical initiatives and delivering enterprise software solutions. Demonstrated success in building high-performing teams and driving organizational growth through innovation and strategic planning."
    elif is_junior:
        summary = f"Motivated professional with solid foundation in software development and problem-solving. Passionate about learning new technologies and contributing to collaborative team environments while building scalable solutions."
    else:
        summary = f"Experienced professional with expertise in software development, team collaboration, and delivering high-quality solutions. Committed to continuous learning and driving technical excellence across cross-functional initiatives."
    
    key_sections = [
        "Professional Summary",
        "Technical Skills",
        "Professional Experience",
        "Education",
        "Certifications & Achievements"
    ]
    
    if any(word in job_description.lower() for word in ["data", "analytics", "database"]):
        suggested_bullets = [
            "Developed and optimized data pipelines processing 100K+ records daily, improving query performance by 40%",
            "Designed scalable database architecture supporting 5M+ concurrent users",
            "Implemented analytics dashboards reducing reporting time by 60%",
            "Led data migration project from legacy systems saving $500K annually",
            "Mentored 3+ junior developers in database optimization best practices"
        ]
    elif any(word in job_description.lower() for word in ["cloud", "aws", "azure", "devops"]):
        suggested_bullets = [
            "Architected and deployed cloud infrastructure on AWS reducing operational costs by 35%",
            "Implemented CI/CD pipelines decreasing deployment time from 2 hours to 15 minutes",
            "Scaled applications to handle 10x traffic increase with zero downtime",
            "Managed containerization strategy using Docker and Kubernetes for 20+ microservices",
            "Reduced infrastructure incidents by 70% through automated monitoring and alerting"
        ]
    elif any(word in job_description.lower() for word in ["frontend", "react", "vue", "angular", "ui"]):
        suggested_bullets = [
            "Built responsive user interfaces with React serving 500K+ daily active users",
            "Improved page load time by 50% through code splitting and lazy loading optimization",
            "Designed and implemented component library increasing dev velocity by 30%",
            "Led frontend accessibility initiative ensuring WCAG 2.1 AA compliance",
            "Mentored team of 4 frontend developers on best practices and code quality standards"
        ]
    else:
        suggested_bullets = [
            "Led development of mission-critical features delivering 30% improvement in user engagement",
            "Architected scalable solutions supporting 10x business growth with 99.9% uptime",
            "Implemented automated testing framework increasing code coverage from 40% to 85%",
            "Collaborated cross-functionally with product, design, and leadership teams to deliver quarterly roadmap",
            "Mentored junior team members and conducted code reviews ensuring quality standards"
        ]
    
    return {
        "summary": summary,
        "key_sections": key_sections,
        "suggested_bullets": suggested_bullets
    }

def analyze_skill_gaps(resume_text: str, job_description: str) -> dict:
    prompt = f"""
    Act as an expert technical recruiter. Analyze the EXACT skills between the candidate's resume and the job requirements.
    Extract and compare specific technical and professional skills.
    Output ONLY a valid JSON object with keys: 
    - "present_skills" (list of 8-10 skills found in resume)
    - "required_skills" (list of 8-10 skills from job description)
    - "missing_skills" (list of 5-8 skills required but not in resume)
    
    Ensure all are valid lists and non-empty.
    
    Job Description:
    {job_description}
    
    Resume Text:
    {resume_text}
    """
    try:
        response_text = _call_gemini_with_retry(prompt)
        if response_text:
            result = json.loads(response_text)
            # Validate and ensure defaults
            if "present_skills" not in result or not isinstance(result["present_skills"], list):
                result["present_skills"] = ["Experience", "Problem Solving", "Technical Skills"]
            if "required_skills" not in result or not isinstance(result["required_skills"], list):
                result["required_skills"] = ["Python", "System Design", "Communication"]
            if "missing_skills" not in result or not isinstance(result["missing_skills"], list):
                result["missing_skills"] = ["Advanced frameworks", "Specialized tools", "Domain expertise"]
            return result
        else:
            return {
                "present_skills": ["Technical Knowledge", "Problem Solving", "Collaboration"],
                "required_skills": ["Python", "AWS", "System Design", "Communication"],
                "missing_skills": ["Advanced specialization", "Specific certifications"]
            }
    except json.JSONDecodeError:
        return {
            "present_skills": ["Job-related skills", "Industry experience", "Technical background"],
            "required_skills": ["Job posting requirements", "Technical skills needed", "Nice-to-have skills"],
            "missing_skills": ["Skills gap identified", "Areas to develop", "Learning opportunities"]
        }
    except Exception as e:
        return {
            "present_skills": ["Core competencies", "Transferable skills"],
            "required_skills": ["Job requirements", "Essential skills"],
            "missing_skills": ["Skills to develop", "Training areas"]
        }