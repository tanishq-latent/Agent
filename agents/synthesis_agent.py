"""
STUDENT GUIDE - AGENT 4: Synthesis & Interview Prep

Agentic Feature: Includes a Hiring Rules Tool to assign badges based on score thresholds.
"""

import json
from agents.base import ask_groq_ai


def _apply_hiring_rules(synthesis: dict, evaluation: dict) -> dict:
    """TOOL: Assigns hiring badge color based on final score."""
    score = float(evaluation.get("raw_total_score", 0))
    synthesis["final_score"] = score

    if score >= 85.0:
        synthesis["overall_recommendation"], synthesis["recommendation_badge_color"] = "STRONG_MATCH", "green"
    elif score >= 70.0:
        synthesis["overall_recommendation"], synthesis["recommendation_badge_color"] = "POTENTIAL_MATCH", "amber"
    else:
        synthesis["overall_recommendation"], synthesis["recommendation_badge_color"] = "UNDERQUALIFIED", "red"

    return synthesis


def synthesize_report(candidate_profile: dict, rubric: dict, evaluation: dict, api_key: str = None) -> dict:
    """Agent 4: Generates hiring synthesis and tailored interview questions."""
    system_prompt = """You are Agent 4: Synthesis & Interview Prep.
Synthesize candidate report into JSON:
{
  "candidate_name": "Candidate Name",
  "overall_recommendation": "STRONG_MATCH",
  "recommendation_badge_color": "green",
  "final_score": 88.5,
  "executive_summary": "2 sentence executive brief.",
  "strengths_summary": ["Strength 1"],
  "areas_for_probing": ["Area 1"],
  "interview_questions": [
    {
      "category": "Technical Deep-Dive",
      "question": "Specific interview question referencing candidate's resume?",
      "context_rationale": "Why are we asking this?",
      "ideal_answer_signals": ["Signal candidate should mention"]
    }
  ]
}"""

    user_prompt = f"PROFILE:\n{json.dumps(candidate_profile)}\n\nRUBRIC:\n{json.dumps(rubric)}\n\nEVALUATION:\n{json.dumps(evaluation)}"

    # 1. Ask AI for summary and interview questions
    raw_synth = ask_groq_ai(system_prompt, user_prompt, api_key=api_key)

    # 2. Run Hiring Rules Tool to set overall recommendation badge
    return _apply_hiring_rules(raw_synth, evaluation)
