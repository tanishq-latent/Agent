"""
STUDENT GUIDE - AGENT 2: Job Rubric Analyzer

Agentic Feature: Includes a 4-line Self-Correction Tool that ensures category weights sum to 100%.
"""

from agents.base import ask_groq_ai


def _fix_weights_to_100(rubric: dict) -> dict:
    """TOOL: Fixes category weights to sum to exactly 100%."""
    categories = rubric.get("rubric_categories", {})
    total = sum(c.get("weight_percent", 0) for c in categories.values())
    if total > 0 and total != 100:
        for c in categories.values():
            c["weight_percent"] = round((c.get("weight_percent", 0) / total) * 100)
    return rubric


def analyze_job_description(jd_text: str, api_key: str = None) -> dict:
    """Agent 2: Converts Job Description into a 100-point rubric and fixes weights."""
    system_prompt = """You are Agent 2: Job Rubric Analyzer.
Convert a Job Description into a JSON evaluation rubric (category weights MUST total 100%):
{
  "job_title": "Target Role Title",
  "min_years_experience": 3,
  "must_have_skills": ["Python", "FastAPI"],
  "nice_to_have_skills": ["Docker", "Groq API"],
  "rubric_categories": {
    "technical_skills": {"weight_percent": 35, "description": "Programming languages & frameworks"},
    "experience_depth": {"weight_percent": 30, "description": "Years & project complexity"},
    "domain_relevance": {"weight_percent": 20, "description": "Industry relevance"},
    "education_certifications": {"weight_percent": 15, "description": "Degree & certs"}
  },
  "dealbreakers": ["Under minimum required experience"]
}"""

    user_prompt = f"JOB DESCRIPTION:\n{jd_text}"

    # 1. Ask AI for initial rubric
    rubric = ask_groq_ai(system_prompt, user_prompt, api_key=api_key)

    # 2. Run Self-Correction Tool to guarantee 100% weight sum
    return _fix_weights_to_100(rubric)
