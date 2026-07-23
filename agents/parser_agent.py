"""
STUDENT GUIDE - AGENT 1: Resume Parser

What does Agent 1 do?
It takes unstructured raw resume text and asks AI to organize it into clean JSON
(Candidate Name, Contact Info, Experience Years, Skills, Work History).
"""

from agents.base import ask_groq_ai


def parse_resume(resume_text: str, filename: str, api_key: str = None) -> dict:
    """Agent 1: Extracts candidate profile details from raw resume text."""
    system_prompt = """You are Agent 1: Resume Parser.
Your job is to read raw resume text and organize it into JSON matching this exact structure:
{
  "candidate_name": "Candidate Full Name",
  "contact": {"email": "email or null", "phone": "phone or null", "location": "location or null"},
  "summary": "2 sentence profile summary",
  "total_years_experience": 4.5,
  "skills": {
    "languages": ["Python", "JavaScript"],
    "frameworks": ["FastAPI", "React"],
    "databases": ["PostgreSQL"],
    "cloud_devops": ["AWS", "Docker"],
    "ai_ml": ["Groq"]
  },
  "work_experience": [
    {
      "company": "Company Name",
      "title": "Job Title",
      "duration": "2022 - Present",
      "responsibilities": ["Key accomplishment 1"],
      "technologies": ["Python"]
    }
  ],
  "education": [{"degree": "B.S. in CS", "institution": "University Name", "year": "2020"}]
}"""

    user_prompt = f"Filename: {filename}\n\nRESUME TEXT:\n{resume_text}"

    # Call AI
    profile = ask_groq_ai(system_prompt, user_prompt, api_key=api_key)
    profile["filename"] = filename
    return profile
