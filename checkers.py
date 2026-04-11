"""Resume quality checkers using Gemini API."""
import time
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

try:
    client = genai.Client()
except Exception as e:
    pass

ESSENTIAL_SECTIONS = {
    "Contact Information": ["email", "phone", "address"],
    "Professional Summary": ["summary", "objective", "professional summary"],
    "Experience": ["experience", "work experience", "employment"],
    "Education": ["education", "degree", "university", "college"],
    "Skills": ["skills", "technical skills", "competencies"]
}

def _call_gemini_with_retry(prompt: str, max_retries: int = 3) -> str:
    """Helper function to call Gemini API with retry logic."""
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
                wait_time = 2 ** attempt
                time.sleep(wait_time)
            else:
                raise e
    return None


def check_essential_sections(resume_text: str) -> dict:
    prompt = f"""
    Analyze this resume and check for the presence of these essential sections:
    1. Contact Information (email, phone, address)
    2. Professional Summary or Objective
    3. Work Experience
    4. Education
    5. Skills

    Resume Text:
    {resume_text}

    Return a JSON with this structure:
    {{
        "sections_found": {{"Contact Information": true/false, "Professional Summary": true/false, "Experience": true/false, "Education": true/false, "Skills": true/false}},
        "missing_sections": [list of missing sections],
        "completeness_score": 0-100,
        "suggestions": [list of suggestions to improve completeness]
    }}
    """
    
    try:
        response = _call_gemini_with_retry(prompt)
        import json
        return json.loads(response)
    except Exception as e:
        return {
            "error": str(e),
            "sections_found": {},
            "missing_sections": [],
            "completeness_score": 0,
            "suggestions": ["Unable to analyze sections. Please try again."]
        }


def check_contact_information(resume_text: str) -> dict:
    prompt = f"""
    Analyze the contact information in this resume. Check if it contains:
    1. Email address (valid format)
    2. Phone number (valid format)
    3. Full name or current location
    4. LinkedIn or Portfolio URL (optional but good)

    Resume Text:
    {resume_text}

    Return a JSON with this structure:
    {{
        "has_email": true/false,
        "has_phone": true/false,
        "has_name": true/false,
        "has_location": true/false,
        "has_linkedin": true/false,
        "email_valid": true/false/null,
        "phone_valid": true/false/null,
        "contact_quality_score": 0-100,
        "issues": [list of issues found],
        "recommendations": [list of recommendations]
    }}
    """
    
    try:
        response = _call_gemini_with_retry(prompt)
        import json
        return json.loads(response)
    except Exception as e:
        return {
            "error": str(e),
            "has_email": False,
            "has_phone": False,
            "has_name": False,
            "contact_quality_score": 0,
            "issues": ["Unable to analyze contact information"],
            "recommendations": []
        }


def check_grammar_and_formatting(resume_text: str) -> dict:
    prompt = f"""
    Analyze this resume for grammar, spelling, and formatting issues.
    
    Resume Text:
    {resume_text}

    Return a JSON with this structure:
    {{
        "grammar_score": 0-100,
        "spelling_score": 0-100,
        "formatting_score": 0-100,
        "overall_quality_score": 0-100,
        "grammar_issues": [list of specific grammar issues found],
        "spelling_errors": [list of spelling errors],
        "formatting_issues": [list of formatting problems],
        "improvements": [list of specific improvement suggestions]
    }}
    """
    
    try:
        response = _call_gemini_with_retry(prompt)
        import json
        return json.loads(response)
    except Exception as e:
        return {
            "error": str(e),
            "grammar_score": 0,
            "spelling_score": 0,
            "formatting_score": 0,
            "overall_quality_score": 0,
            "grammar_issues": ["Unable to analyze grammar"],
            "spelling_errors": [],
            "formatting_issues": [],
            "improvements": []
        }


def run_all_checks(resume_text: str) -> dict:
    return {
        "sections": check_essential_sections(resume_text),
        "contact": check_contact_information(resume_text),
        "grammar": check_grammar_and_formatting(resume_text)
    }
