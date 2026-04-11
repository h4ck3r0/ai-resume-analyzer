import re
import json


def _call_gemini_with_retry(prompt: str, max_retries: int = 3) -> str:
    
    from google import genai
    import time
    
    for attempt in range(max_retries):
        try:
            client = genai.Client()
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=prompt
            )
            return response.text
        except Exception as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt
                time.sleep(wait_time)
            else:
                raise e
    return None

ACTION_VERBS = [
    'Achieved', 'Built', 'Created', 'Designed', 'Developed', 'Directed',
    'Engineered', 'Enhanced', 'Expanded', 'Implemented', 'Improved',
    'Increased', 'Launched', 'Led', 'Managed', 'Optimized', 'Orchestrated',
    'Pioneered', 'Produced', 'Programmed', 'Proposed', 'Reduced', 'Redesigned',
    'Refactored', 'Reorganized', 'Scaled', 'Spearheaded', 'Streamlined', 'Transformed'
]


def extract_education(text: str) -> list:
    education = []
    degree_patterns = [
        r"(?:bachelor|b\.?s\.?|b\.?a\.?|master|m\.?s\.?|m\.?b\.?a\.?|phd|ph\.?d\.?|doctorate).*?(?:in|of)?\s+([a-z\s]+?)(?:\s+from|\s+at|\n|$)",
        r"(?:from|at)?\s*([A-Z][a-z\s]+(?:University|College|Institute|School)).*?(?:\d{4})?",
    ]
    
    for pattern in degree_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        education.extend(matches[:2])
    
    return list(dict.fromkeys(education))[:3]  # Return unique, max 3


def extract_work_experience(text: str) -> list:
    experience = []
    
    job_patterns = [
        r"(?:Senior|Junior|Lead)?\s*([A-Z][a-z\s]+(?:Engineer|Developer|Manager|Analyst|Designer|Architect))",
        r"(?:at|with|company:?)\s*([A-Z][a-zA-Z\s&,\.]+?)(?:\n|\s{2,}|$)"
    ]
    
    for pattern in job_patterns:
        matches = re.findall(pattern, text)
        experience.extend(matches[:2])
    
    return list(dict.fromkeys(experience))[:5]  # Return unique, max 5


def extract_contact_info(text: str) -> dict:
    contact = {
        'phone': None,
        'linkedin': None,
        'github': None,
        'website': None
    }
    
  
    phone_match = re.search(r'(?:\+?1[-.\s]?)?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})', text)
    if phone_match:
        contact['phone'] = f"{phone_match.group(1)}-{phone_match.group(2)}-{phone_match.group(3)}"
    
   
    linkedin_match = re.search(r'linkedin\.com/in/([a-z0-9\-]+)', text, re.IGNORECASE)
    if linkedin_match:
        contact['linkedin'] = linkedin_match.group(1)
    
  
    github_match = re.search(r'github\.com/([a-z0-9\-]+)', text, re.IGNORECASE)
    if github_match:
        contact['github'] = github_match.group(1)
    
  
    website_match = re.search(r'(?:www\.)?([a-z0-9\-]+\.(?:com|io|dev|co))', text, re.IGNORECASE)
    if website_match:
        contact['website'] = website_match.group(1)
    
    return {k: v for k, v in contact.items() if v}


def analyze_ats_compliance(text: str) -> dict:
    issues = []
    score = 100
    
    if len(text) < 200:
        issues.append("Resume may be too short for proper ATS parsing")
        score -= 15
    
    if '|' in text and text.count('|') > 5:
        issues.append("Excessive use of special characters or tables detected")
        score -= 10
    
    if not re.search(r'(experience|education|skills)', text, re.IGNORECASE):
        issues.append("Missing standard resume sections")
        score -= 10
    
    if len(text.split('\n')) < 10:
        issues.append("Poor formatting - resume appears compressed")
        score -= 5
    
    return {
        'score': max(score, 0),
        'issues': issues[:3] if issues else ['No major ATS issues detected']
    }


def analyze_keyword_match(resume_text: str, job_description: str) -> list:
    if not job_description:
        return []
    
    prompt = f"""
    Extract the most important technical and professional keywords from the job description below.
    Focus on:
    - Programming languages and frameworks (e.g., Python, Flask, Django)
    - Technologies and tools (e.g., Git, Docker, AWS)
    - Skills and concepts (e.g., machine learning, data analysis)
    - Key terms and buzzwords
    - Location-specific information if relevant
    
    Output ONLY a JSON array of the 20 most important keywords (lowercase), nothing else.
    Example: ["python", "flask", "machine learning", "aws", "docker"]
    
    Job Description:
    {job_description}
    """
    
    try:
        response_text = _call_gemini_with_retry(prompt)
        if response_text:
            keywords_list = json.loads(response_text)
            resume_lower = resume_text.lower()
            
            matched_keywords = [kw for kw in keywords_list if kw.lower() in resume_lower]
            
            return matched_keywords[:15]
    except Exception as e:
        pass
    
    common_words = {'the', 'and', 'for', 'with', 'your', 'will', 'able', 'from', 'that', 'this', 'team',
                   'good', 'strong', 'we', 'are', 'have', 'has', 'must', 'should', 'or', 'an', 'also', 'as'}
    
    job_words = set(re.findall(r'\b([a-z]{3,})\b', job_description.lower()))
    job_words = {w for w in job_words if w not in common_words}
    
    resume_text_lower = resume_text.lower()
    matched_keywords = [w for w in sorted(job_words) if w in resume_text_lower]
    
    return matched_keywords[:15]


def analyze_action_verbs(text: str) -> dict:
    text_lower = text.lower()
    found_verbs = []
    
    for verb in ACTION_VERBS:
        if verb.lower() in text_lower:
            count = len(re.findall(r'\b' + verb.lower() + r'\b', text_lower))
            found_verbs.append((verb, count))
    
    found_verbs.sort(key=lambda x: x[1], reverse=True)
    
    total_action_verbs = sum(count for _, count in found_verbs)
    percentage = int((total_action_verbs / max(len(text.split()), 1)) * 100)
    
    return {
        'found': found_verbs[:5],
        'total_count': total_action_verbs,
        'score': min(percentage, 100)
    }


def analyze_quantification(text: str) -> dict:
    lines = text.split('\n')
    bullet_lines = [l for l in lines if l.strip().startswith('-') or l.strip().startswith('•')]
    
    if not bullet_lines:
        return {'score': 0, 'message': 'No bullet points found'}
    
    quantified = [line for line in bullet_lines if re.search(r'\d+[%,.\d]*|\$\d+', line)]
    percentage = int((len(quantified) / len(bullet_lines)) * 100)
    
    return {
        'score': percentage,
        'quantified_bullets': len(quantified),
        'total_bullets': len(bullet_lines),
        'message': f"{percentage}% of bullets contain metrics or numbers"
    }


def analyze_length_and_format(text: str) -> dict:
    word_count = len(text.split())
    line_count = len(text.split('\n'))
    
    if word_count < 250:
        length_score = 50
        length_msg = "Resume is too short (ideal: 250-600 words)"
    elif word_count > 1000:
        length_score = 60
        length_msg = "Resume may be too long (ideal: 250-600 words)"
    else:
        length_score = 100
        length_msg = "Good length for resume"
    
    return {
        'word_count': word_count,
        'line_count': line_count,
        'length_score': length_score,
        'message': length_msg
    }
