from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Lazy load model to save memory at startup
_model = None

def _get_model():
    """Lazy load the sentence transformer model."""
    global _model
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    return _model

def calculate_semantic_match(resume_text: str, job_description: str) -> float:
    """
    Calculates the ATS match score using Cosine Similarity between vector embeddings.
    """
    if not resume_text or not job_description:
        return 0.0

    model = _get_model()
    embeddings = model.encode([resume_text, job_description])
    
    resume_vector = embeddings[0].reshape(1, -1)
    jd_vector = embeddings[1].reshape(1, -1)
    
    similarity_score = cosine_similarity(resume_vector, jd_vector)[0][0]
    percentage_score = max(0, round(similarity_score * 100, 2))
    
    return percentage_score

def benchmark_score(score: float) -> dict:
    """Benchmarks a score against industry standards and returns performance data."""
    benchmarks = {
        "industry_average": 72.0,
        "excellent_threshold": 85.0,
        "good_threshold": 70.0,
        "needs_improvement_threshold": 50.0
    }
    
    if score >= benchmarks["excellent_threshold"]:
        rating = "Excellent"
        percentile = 90
    elif score >= benchmarks["good_threshold"]:
        rating = "Good"
        percentile = 70
    elif score >= benchmarks["needs_improvement_threshold"]:
        rating = "Needs Improvement"
        percentile = 40
    else:
        rating = "Poor"
        percentile = 10
    
    return {
        "score": score,
        "rating": rating,
        "percentile": percentile,
        "industry_average": benchmarks["industry_average"],
        "comparison": "Above" if score >= benchmarks["industry_average"] else "Below"
    }