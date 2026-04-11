import re
import json


def _detect_resume_sections(text: str) -> dict:
    """Detect major resume sections and their locations in the text."""
    sections = {}
    section_patterns = {
        'contact': r'(?:contact|email|phone|address|linkedin|github)',
        'summary': r'(?:professional\s+summary|summary|objective|profile)',
        'skills': r'(?:technical\s+skills|skills|competencies|expertise)',
        'experience': r'(?:work\s+experience|professional\s+experience|experience|employment)',
        'education': r'(?:education|academic|degree|university|college)',
        'projects': r'(?:projects|portfolio|side\s+projects)',
        'certifications': r'(?:certifications|licenses|achievements|awards)',
    }
    
    # Find positions of each section
    for section_name, pattern in section_patterns.items():
        for match in re.finditer(pattern, text, re.IGNORECASE):
            sections[section_name] = match.start()
    
    return sections


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
    """Extract education information using LLM with regex fallback."""
    if not text:
        return []
    
    # Try LLM-based extraction first
    prompt = f"""
    Extract ONLY the education section from this resume.
    List each degree, field of study, and institution found.
    Return as a JSON array of strings, each entry in format: "Degree - Field of Study from Institution (Year if available)"
    Only return the array, nothing else.
    Example: ["Bachelor of Science in Computer Science from Stanford University (2020)", "Master of Science in Machine Learning from MIT"]
    If no education found, return empty array: []
    
    Resume Text:
    {text}
    """
    
    try:
        response_text = _call_gemini_with_retry(prompt)
        if response_text:
            education = json.loads(response_text)
            if isinstance(education, list) and len(education) > 0:
                return education[:5]  # Return max 5 entries
    except (json.JSONDecodeError, Exception):
        pass
    
    # Fallback to improved regex patterns
    education = []
    
    # Pattern for degree types and fields
    degree_patterns = [
        r"(?:bachelor|b\.s\.|b\.a\.|master|m\.s\.|m\.b\.a\.|phd|doctorate|d\.d\.s\.|md)\s+(?:in|of|–|—)?\s*([a-z&\s,]+?)(?:\s+from|\s+at|\n|—|–|\d{4}|$)",
        r"(?:from|at)?\s*([A-Z][a-z\s&,]+?(?:University|College|Institute|School|Academy|Institute of Technology))(?:\s+\(|\n|\d{4})?",
    ]
    
    for pattern in degree_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        education.extend([m.strip() for m in matches if m.strip()])
    
    # Remove duplicates and return
    return list(dict.fromkeys(education))[:5]


def extract_work_experience(text: str) -> list:
    """Extract work experience using LLM with regex fallback."""
    if not text:
        return []
    
    # Try LLM-based extraction first
    prompt = f"""
    Extract ONLY the work experience/professional experience section from this resume.
    For each position, list: Job Title at Company (Duration if available)
    Return as a JSON array of strings.
    Only return the array, nothing else.
    Example: ["Senior Software Engineer at Google (2020-2024)", "Full Stack Developer at Startup Inc (2018-2020)"]
    If no work experience found, return empty array: []
    
    Resume Text:
    {text}
    """
    
    try:
        response_text = _call_gemini_with_retry(prompt)
        if response_text:
            experience = json.loads(response_text)
            if isinstance(experience, list) and len(experience) > 0:
                return experience[:8]  # Return max 8 entries
    except (json.JSONDecodeError, Exception):
        pass
    
    # Fallback to improved regex patterns
    experience = []
    
    job_title_pattern = r"(?:^|\n)\s*([A-Z][a-z\s]*?(?:Engineer|Developer|Manager|Analyst|Designer|Architect|Director|Lead|Specialist|Consultant|Officer|Executive|Administrator|Coordinator|Technician)[a-z\s]*?)(?:\s+at|\s+–|\s+-|$)"
    
    company_pattern = r"(?:at|with|company\s*[:=]?)\s*([A-Z][a-zA-Z\s&,\.'-]+?)(?:\n|$|\s+\(|\s+\d{4})"
    
    job_titles = re.findall(job_title_pattern, text, re.IGNORECASE | re.MULTILINE)
    companies = re.findall(company_pattern, text)
    
    # Combine job titles and companies
    for title in job_titles[:5]:
        if title.strip():
            experience.append(title.strip())
    
    for company in companies[:5]:
        if company.strip() and company.strip() not in experience:
            experience.append(company.strip())
    
    return list(dict.fromkeys(experience))[:8]


def extract_contact_info(text: str) -> dict:
    """Extract contact information with improved regex patterns."""
    contact = {
        'phone': None,
        'email': None,
        'linkedin': None,
        'github': None,
        'website': None
    }
    
    # Extract email - improved pattern
    email_match = re.search(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
    if email_match:
        contact['email'] = email_match.group(0)
    
    # Extract phone - improved pattern for various formats
    phone_patterns = [
        r'(?:\+?1[-.\s]?)?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})',  # US format
        r'\+\d{1,3}\s?\d{1,14}',  # International format
        r'\(?(\d{10})\)?'  # 10 digit format
    ]
    
    for pattern in phone_patterns:
        phone_match = re.search(pattern, text)
        if phone_match:
            if len(phone_match.groups()) >= 3:
                contact['phone'] = f"{phone_match.group(1)}-{phone_match.group(2)}-{phone_match.group(3)}"
            else:
                contact['phone'] = phone_match.group(0)
            break
    
    # Extract LinkedIn profile
    linkedin_match = re.search(r'(?:linkedin\.com/in/|linkedin:|user:)\s*([a-z0-9\-]+)', text, re.IGNORECASE)
    if linkedin_match:
        contact['linkedin'] = linkedin_match.group(1)
    
    # Extract GitHub profile
    github_match = re.search(r'(?:github\.com/|github:|@)\s*([a-z0-9\-]+)', text, re.IGNORECASE)
    if github_match:
        contact['github'] = github_match.group(1)
    
    # Extract website/portfolio
    website_patterns = [
        r'(?:website|portfolio)\s*[:=]?\s*(https?://[^\s]+)',
        r'(?:www\.)?([a-z0-9\-]+\.(?:com|io|dev|co|net|org))',
    ]
    
    for pattern in website_patterns:
        website_match = re.search(pattern, text, re.IGNORECASE)
        if website_match:
            contact['website'] = website_match.group(1) if '://' not in website_match.group(1) else website_match.group(1)
            break
    
    return {k: v for k, v in contact.items() if v is not None}


def analyze_ats_compliance(text: str) -> dict:
    """Analyze ATS compliance with more detailed checks."""
    issues = []
    score = 100
    
    # Check length
    word_count = len(text.split())
    if word_count < 200:
        issues.append("Resume too short - ATS parsing may fail (minimum 200 words recommended)")
        score -= 15
    elif word_count > 1500:
        issues.append("Resume possibly too long - may overwhelm ATS systems (maximum 1500 words recommended)")
        score -= 10
    
    # Check for problematic characters
    if text.count('|') > 10:
        issues.append("Excessive use of pipes/special characters - use clean formatting for ATS")
        score -= 15
    
    if text.count('•') > 20 or text.count('°') > 5:
        issues.append("Special bullet characters may not parse correctly - use standard bullets or dashes")
        score -= 10
    
    # Check for standard sections
    required_sections = ['experience', 'education', 'skills']
    found_sections = sum(1 for section in required_sections if re.search(section, text, re.IGNORECASE))
    
    if found_sections < 2:
        issues.append("Missing standard resume sections - ensure Education, Experience, and Skills are included")
        score -= 20
    
    # Check for proper line breaks
    lines = text.split('\n')
    if len(lines) < 12:
        issues.append("Poor formatting - resume appears overly compressed without proper line breaks")
        score -= 10
    
    # Check for email presence
    if not re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text):
        issues.append("No email address found - critical for ATS to contact you")
        score -= 15
    
    # Check for contact info
    if not re.search(r'\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', text):
        issues.append("Phone number not formatted clearly - ensure standard format (XXX-XXX-XXXX)")
        score -= 5
    
    return {
        'score': max(score, 0),
        'issues': issues[:5] if issues else ['ATS compliance looks good - resume should parse correctly'],
        'word_count': word_count
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
