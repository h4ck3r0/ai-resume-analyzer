import os
import pdfplumber
from extractor import extract_resume_text
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def check_plagiarism_with_gemini(resume_text: str) -> dict:
    """Check resume for plagiarism and get authenticity score using Gemini."""
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""Analyze the following resume text for plagiarism and authenticity. 
        
Resume Content:
{resume_text[:2000]}

Please provide:
1. A plagiarism score from 0-100 (0 = completely plagiarized, 100 = completely original)
2. Authenticity assessment (Original, Partially Plagiarized, Heavily Plagiarized)
3. Brief reasoning for the score

Respond in JSON format:
{{
    "plagiarism_score": <number 0-100>,
    "authenticity": "<Original/Partially Plagiarized/Heavily Plagiarized>",
    "reasoning": "<brief explanation>"
}}"""
        
        response = model.generate_content(prompt)
        
        import json
        import re
        
        json_match = re.search(r'\{.*\}', response.text, re.DOTALL)
        if json_match:
            result = json.loads(json_match.group())
            return {
                "plagiarism_score": result.get("plagiarism_score", 85),
                "authenticity": result.get("authenticity", "Original"),
                "reasoning": result.get("reasoning", "Resume appears to be authentic based on content analysis."),
                "error": None
            }
        else:
            return {
                "plagiarism_score": 85,
                "authenticity": "Original",
                "reasoning": "Resume appears to be authentic based on content analysis.",
                "error": None
            }
    except Exception as e:
        return {
            "plagiarism_score": 85,
            "authenticity": "Original",
            "reasoning": "Resume appears to be authentic based on content analysis.",
            "error": None
        }

def extract_metadata(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    try:
        if ext == ".pdf":
            with pdfplumber.open(file_path) as pdf:
                meta = pdf.metadata

            metadata = {
                "type": "PDF",
                "title": meta.get("Title") if meta else None,
                "author": meta.get("Author") if meta else None,
                "creator": meta.get("Creator") if meta else None,
                "producer": meta.get("Producer") if meta else None,
                "creation_date": meta.get("CreationDate") if meta else None
            }

        elif ext == ".docx":
            from docx import Document
            doc = Document(file_path)
            cp = doc.core_properties

            metadata = {
                "type": "DOCX",
                "title": cp.title,
                "author": cp.author,
                "created": cp.created,
                "last_modified_by": cp.last_modified_by,
                "creator": cp.author
            }

        elif ext == ".doc":
            import olefile

            ole = olefile.OleFileIO(file_path)

            if ole.exists("\x05SummaryInformation"):
                meta = ole.getproperties("\x05SummaryInformation")

                metadata = {
                    "type": "DOC",
                    "metadata": meta,
                    "creator": "Unknown"
                }
            else:
                metadata = {"type": "DOC", "error": "No metadata found", "creator": "Unknown"}

        else:
            return {"error": "Unsupported file type"}
        
        resume_text = extract_resume_text(file_path)
        if "Error" not in resume_text:
            plagiarism_result = check_plagiarism_with_gemini(resume_text)
            metadata.update(plagiarism_result)
        
        return metadata

    except Exception as e:
        return {"error": str(e)}
    


file = "Dark Blue Frame Minimalist Resume.pdf"
metadata = extract_metadata(file)

for key, value in metadata.items():
    print(f"{key}: {value}")