"""
STUDENT GUIDE - AGENT 3: Candidate Evaluator

Agentic Feature: Includes a Math Calculator Tool to calculate exact weighted scores in Python.
"""

import json
from agents.base import ask_groq_ai


def _calculate_exact_scores(evaluation: dict) -> dict:
    """TOOL: Calculates exact weighted scores in Python."""
    total = 0.0
    for c in evaluation.get("category_evaluations", {}).values():
        score = float(c.get("score", 0))
        weight = float(c.get("weight_percent", 0))
        c["weighted_score"] = round((score * weight) / 100.0, 2)
        total += c["weighted_score"]
    evaluation["raw_total_score"] = round(total, 2)
    return evaluation


def evaluate_candidate(candidate_profile: dict, rubric: dict, api_key: str = None) -> dict:
    """Agent 3: Scores candidate profile against rubric and calculates exact math."""
    system_prompt = """You are Agent 3: Candidate Evaluator.
Compare candidate profile against Job Rubric. Return JSON:
{
  "candidate_name": "Candidate Name",
  "category_evaluations": {
    "technical_skills": {
      "score": 90, "weight_percent": 35, "weighted_score": 31.5,
      "justification": "Explanation of score",
      "matched_skills": ["Python"], "missing_skills": [],
      "evidence_quotes": ["Exact quote from resume"]
    },
    "experience_depth": {"score": 85, "weight_percent": 30, "weighted_score": 25.5, "justification": "Explanation", "evidence_quotes": []},
    "domain_relevance": {"score": 90, "weight_percent": 20, "weighted_score": 18.0, "justification": "Explanation", "evidence_quotes": []},
    "education_certifications": {"score": 90, "weight_percent": 15, "weighted_score": 13.5, "justification": "Explanation", "evidence_quotes": []}
  },
  "raw_total_score": 88.5,
  "red_flags": [{"severity": "LOW", "flag": "Missing nice-to-have skill", "impact": "Low risk"}],
  "green_flags": [{"flag": "Reduced latency by 45%", "evidence": "Quote from resume"}]
}"""

    user_prompt = f"RUBRIC:\n{json.dumps(rubric)}\n\nCANDIDATE PROFILE:\n{json.dumps(candidate_profile)}"

    # 1. Ask AI for scores and quote evidence
    raw_eval = ask_groq_ai(system_prompt, user_prompt, api_key=api_key)

    # 2. Run Math Calculator Tool for 100% accurate weighted scores
    return _calculate_exact_scores(raw_eval)
