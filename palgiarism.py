import os
import pdfplumber
from extractor import extract_resume_text
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def check_plagiarism_with_gemini(resume_text: str, creator: str = None) -> dict:
    """Check resume for plagiarism and get authenticity score using Gemini."""
    try:
        import json
        import re
        
        model = genai.GenerativeModel('gemini-pro')
        
        prompt = f"""You are a plagiarism detector. Analyze this resume carefully for authenticity and originality.

Resume Content:
{resume_text[:3000]}

Created with: {creator if creator else 'Unknown'}

Analyze and provide ONLY a JSON response (no other text):
{{
    "plagiarism_score": <integer 0-100 where 100=original, 0=plagiarized>,    
    "authenticity": "<Original|Partially Plagiarized|Heavily Plagiarized>",
    "reasoning": "<2-3 sentence explanation>"
}}

IMPORTANT: If the resume is from a template tool like Canva, score should be LOW (20-40). Return ONLY the JSON."""
        
        response = model.generate_content(prompt)
        response_text = response.text.strip()
        
        # Extract JSON from response
        json_match = re.search(r'\{[^{}]*(?:"[^"]*"[^{}]*)*\}', response_text)
        
        if json_match:
            try:
                result = json.loads(json_match.group())
                plagiarism_score = int(result.get("plagiarism_score", 50))
                authenticity = result.get("authenticity", "Unknown").strip()
                reasoning = result.get("reasoning", "Analysis completed.").strip()
                
                return {
                    "plagiarism_score": plagiarism_score,
                    "authenticity": authenticity,
                    "reasoning": reasoning,
                    "error": None
                }
            except (json.JSONDecodeError, ValueError) as parse_error:
                # If it's from a known template creator, mark as plagiarized
                if creator and any(template in creator.lower() for template in ['canva', 'template', 'resume builder']):
                    return {
                        "plagiarism_score": 35,
                        "authenticity": "Partially Plagiarized",
                        "reasoning": f"Resume appears to be from a template tool ({creator}). Contains pre-designed content.",
                        "error": None
                    }
                return {
                    "plagiarism_score": 50,
                    "authenticity": "Unknown",
                    "reasoning": "Unable to fully analyze. Please review manually.",
                    "error": None
                }
        else:
            # If creator is from known template tool
            if creator and any(template in creator.lower() for template in ['canva', 'template', 'resume builder']):
                return {
                    "plagiarism_score": 35,
                    "authenticity": "Partially Plagiarized",
                    "reasoning": f"Resume appears to be from a template tool ({creator}). Contains pre-designed content and formatting.",
                    "error": None
                }
            
            return {
                "plagiarism_score": 50,
                "authenticity": "Unknown",
                "reasoning": "Unable to parse AI response. Please review manually.",
                "error": None
            }
    except Exception as e:
        # If creator is from known template tool
        if creator and any(template in creator.lower() for template in ['canva', 'template', 'resume builder']):
            return {
                "plagiarism_score": 35,
                "authenticity": "Partially Plagiarized",
                "reasoning": f"Resume appears to be from a template tool ({creator}). Contains pre-designed content.",
                "error": None
            }
        return {
            "plagiarism_score": 50,
            "authenticity": "Unknown",
            "reasoning": "Analysis service temporarily unavailable. Please try again.",
            "error": str(e)
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
            plagiarism_result = check_plagiarism_with_gemini(resume_text, metadata.get("creator"))
            metadata.update(plagiarism_result)
        
        return metadata

    except Exception as e:
        return {"error": str(e)}
    


file = "Dark Blue Frame Minimalist Resume.pdf"
metadata = extract_metadata(file)

for key, value in metadata.items():
    print(f"{key}: {value}")