import os
import sys

USE_TEXTBLOB = os.getenv("USE_TEXTBLOB", "true").lower() == "true"

try:
    from textblob import TextBlob
    import nltk
    TEXTBLOB_AVAILABLE = True
    try:
        nltk.download('brown', quiet=True)
        nltk.download('punkt', quiet=True)
    except:
        pass
except ImportError:
    TEXTBLOB_AVAILABLE = False
    print("TextBlob not installed. Using simple fallback analysis.")



def check_grammar_with_gemma(resume_text: str) -> dict:
    """
    Check grammar using TextBlob (free, open source) or fallback to simple analysis.
    
    Works on ALL hosting platforms with zero external API calls.
    
    Args:
        resume_text: The full resume text to analyze
        
    Returns:
        Dictionary with detailed grammar and formatting feedback
    """
    
    if USE_TEXTBLOB and TEXTBLOB_AVAILABLE:
        return _check_with_textblob(resume_text)
    else:
        return _check_with_simple_analysis(resume_text)


def _check_with_textblob(resume_text: str) -> dict:
    """
    Use TextBlob for FREE spelling and grammar checking.
    No internet connection needed - runs locally!
    """
    try:
        blob = TextBlob(resume_text)
        
        spelling_errors = []
        corrections = []
        
        for word, correction in blob.spellcheck():
            if word != correction:
                spelling_errors.append(word)
                corrections.append({
                    "type": "spelling",
                    "location": f"Word: {word}",
                    "issue": f"Misspelled: '{word}'",
                    "fix": f"Change to: '{correction}'"
                })
        
       
        grammar_issues = []
        improvements = []
        
        sentences = blob.sentences
        for sentence in sentences:
            sentence_text = str(sentence).lower()
            
            
            weak_verbs = ['was', 'were', 'is', 'are', 'be']
            for verb in weak_verbs:
                if f" {verb} " in sentence_text:
                    grammar_issues.append(f"Passive voice: use strong action verb instead of '{verb}'")
                    improvements.append({
                        "type": "grammar",
                        "location": str(sentence)[:50],
                        "issue": f"Weak verb: '{verb}'",
                        "fix": "Use action verb: Implemented, Developed, Led, Achieved, Managed"
                    })
                    break
        
       
        sentences_text = ' '.join([str(s) for s in sentences])
        has_metrics = any(char.isdigit() for char in sentences_text)
        
        if not has_metrics:
            improvements.append({
                "type": "grammar",
                "location": "Achievement statements",
                "issue": "No quantifiable metrics",
                "fix": "Add numbers: 'Increased by 25%', 'Reduced time by 40%', 'Led 3 teams'"
            })
        
      
        formatting_issues = []
        lines = resume_text.split('\n')
        has_bullet_points = any(line.strip().startswith('-') or line.strip().startswith('•') for line in lines)
        
        if not has_bullet_points and len(lines) > 5:
            formatting_issues.append("Missing bullet points for readability")
            improvements.append({
                "type": "formatting",
                "location": "Experience section",
                "issue": "No bullet points",
                "fix": "Use - or • to structure achievements"
            })
        
   
        spelling_score = max(75, 100 - (len(spelling_errors) * 8))
        grammar_score = max(70, 100 - (len(grammar_issues) * 5))
        formatting_score = max(70, 100 - (len(formatting_issues) * 5))
        overall_score = int((spelling_score + grammar_score + formatting_score) / 3)
        
       
        if len(improvements) < 3:
            improvements.extend([
                {"type": "grammar", "location": "All sections", "issue": "Generic phrasing", "fix": "Use more powerful action verbs"},
                {"type": "formatting", "location": "All dates", "issue": "Date consistency", "fix": "Use consistent format: MM/YYYY"},
                {"type": "grammar", "location": "Experience", "issue": "Impact missing", "fix": "Show business impact in all bullets"}
            ])
        
        return {
            "grammar_score": grammar_score,
            "spelling_score": spelling_score,
            "formatting_score": formatting_score,
            "overall_quality_score": overall_score,
            "grammar_issues": grammar_issues if grammar_issues else ["None found"],
            "spelling_errors": [f"'{e}'" for e in spelling_errors] if spelling_errors else ["None found"],
            "formatting_issues": formatting_issues if formatting_issues else ["None found"],
            "improvements": improvements[:8]
        }
        
    except Exception as e:
        print(f"TextBlob error: {str(e)}. Using fallback analysis.")
        return _check_with_simple_analysis(resume_text)


def _check_with_simple_analysis(resume_text: str) -> dict:
    """
    Fallback: Simple grammar and formatting analysis without external models.
    """
    lines = resume_text.split('\n')
    
    sentences = [s.strip() for s in resume_text.split('.') if s.strip()]
    
    grammar_issues = []
    spelling_errors = []
    formatting_issues = []
    improvements = []
    
    weak_verbs = ['was', 'were', 'is', 'are', 'be']
    for line in lines:
        if any(f" {verb} " in line.lower() for verb in weak_verbs):
            grammar_issues.append("Use action verbs instead of passive voice")
            improvements.append({
                "type": "grammar",
                "location": "Throughout resume",
                "issue": f"Passive voice detected",
                "fix": "Use strong action verbs (e.g., 'Implemented', 'Developed', 'Led')"
            })
            break
    
    has_bullet_points = any(line.strip().startswith('-') or line.strip().startswith('•') for line in lines)
    has_numbers = any(line.strip()[0].isdigit() for line in lines if line.strip())
    
    if not has_bullet_points:
        formatting_issues.append("Missing bullet points for better readability")
        improvements.append({
            "type": "formatting",
            "location": "Experience/Projects section",
            "issue": "No bullet points found",
            "fix": "Use bullet points (- or •) to structure achievements"
        })
    
    has_metrics = any(any(char.isdigit() for char in line) for line in lines)
    if not has_metrics:
        grammar_issues.append("Add quantifiable metrics to demonstrate impact")
        improvements.append({
            "type": "grammar",
            "location": "Achievement descriptions",
            "issue": "Missing quantifiable results",
            "fix": "Include numbers: 'Increased by 25%', 'Reduced time by 40%'"
        })
    
    common_typos = {
        'recieve': 'receive',
        'occured': 'occurred',
        'seperate': 'separate',
        'untill': 'until',
        'managment': 'management'
    }
    
    for typo, correct in common_typos.items():
        if typo.lower() in resume_text.lower():
            spelling_errors.append(f"'{typo}' should be '{correct}'")
            improvements.append({
                "type": "spelling",
                "location": "Resume",
                "issue": f"Misspelled: {typo}",
                "fix": f"Change to: {correct}"
            })
    
    if not improvements:
        improvements = [
            {"type": "grammar", "location": "All sections", "issue": "Generic phrasing", "fix": "Use more powerful action verbs"},
            {"type": "formatting", "location": "All sections", "issue": "Consistency", "fix": "Ensure consistent date and formatting"},
            {"type": "grammar", "location": "Achievements", "issue": "Missing metrics", "fix": "Quantify accomplishments with numbers"}
        ]
    
    grammar_score = max(70, 100 - (len(grammar_issues) * 5))
    spelling_score = max(85, 100 - (len(spelling_errors) * 8))
    formatting_score = max(65, 100 - (len(formatting_issues) * 5))
    overall_score = int((grammar_score + spelling_score + formatting_score) / 3)
    
    return {
        "grammar_score": grammar_score,
        "spelling_score": spelling_score,
        "formatting_score": formatting_score,
        "overall_quality_score": overall_score,
        "grammar_issues": grammar_issues if grammar_issues else ["None found"],
        "spelling_errors": spelling_errors if spelling_errors else ["None found"],
        "formatting_issues": formatting_issues if formatting_issues else ["None found"],
        "improvements": improvements
    }


def _validate_grammar_result(data: dict) -> dict:
    """Validate and normalize grammar check results."""
    defaults = {
        "grammar_score": 75,
        "spelling_score": 85,
        "formatting_score": 70,
        "overall_quality_score": 77,
        "grammar_issues": [],
        "spelling_errors": [],
        "formatting_issues": [],
        "improvements": []
    }
    
    for key, default in defaults.items():
        if key not in data:
            data[key] = default
        elif isinstance(default, list) and not isinstance(data[key], list):
            data[key] = default
    
    for score_key in ['grammar_score', 'spelling_score', 'formatting_score', 'overall_quality_score']:
        if isinstance(data[score_key], (int, float)):
            data[score_key] = max(0, min(100, int(data[score_key])))
        else:
            data[score_key] = defaults[score_key]
    
    return data
