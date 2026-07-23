"""
STUDENT GUIDE - PIPELINE CONTROLLER (services/pipeline.py)

What does this file do?
It connects all 4 agents in a simple 4-step sequence:
Step 1: Run Agent 2 (Rubric Analyzer) on the Job Description once.
Step 2: Loop through each resume:
        - Run Agent 1 (Resume Parser)
        - Run Agent 3 (Candidate Evaluator)
        - Run Agent 4 (Synthesis & Interview Prep)
Step 3: Sort all candidate results by score (highest score first).
"""

import time
from typing import Dict, Any, List, Optional
from agents.parser_agent import parse_resume
from agents.rubric_agent import analyze_job_description
from agents.evaluator_agent import evaluate_candidate
from agents.synthesis_agent import synthesize_report


def run_screening_pipeline(jd_text: str, resumes: List[Dict[str, str]], api_key: Optional[str] = None) -> Dict[str, Any]:
    """Orchestrates all 4 AI agents sequentially."""
    start_time = time.time()

    # -----------------------------------------------------------------
    # STEP 1: Agent 2 analyzes Job Description and creates Rubric
    # -----------------------------------------------------------------
    rubric = analyze_job_description(jd_text, api_key=api_key)

    # -----------------------------------------------------------------
    # STEP 2: Loop through every resume and run Agents 1, 3, and 4
    # -----------------------------------------------------------------
    candidates_results = []

    for item in resumes:
        filename = item["filename"]
        resume_text = item["text"]

        # Agent 1: Parse resume into structured candidate profile
        profile = parse_resume(resume_text, filename, api_key=api_key)
        candidate_name = profile.get("candidate_name", filename)

        # Agent 3: Evaluate candidate profile against rubric
        evaluation = evaluate_candidate(profile, rubric, api_key=api_key)

        # Agent 4: Synthesize report and generate tailored interview questions
        synthesis = synthesize_report(profile, rubric, evaluation, api_key=api_key)

        # Collect candidate result object
        candidates_results.append({
            "filename": filename,
            "candidate_name": candidate_name,
            "parsed_profile": profile,
            "evaluation": evaluation,
            "synthesis": synthesis,
            "final_score": synthesis.get("final_score", evaluation.get("raw_total_score", 0)),
            "recommendation": synthesis.get("overall_recommendation", "POTENTIAL_MATCH"),
            "badge_color": synthesis.get("recommendation_badge_color", "amber"),
            "agent_logs": [
                {"agent": "Agent 1 (Parser)", "message": f"Parsed profile for {candidate_name}"},
                {"agent": "Agent 3 (Evaluator)", "message": f"Scored {evaluation.get('raw_total_score', 0)}/100"},
                {"agent": "Agent 4 (Synthesis)", "message": f"Recommendation: {synthesis.get('overall_recommendation')}"}
            ]
        })

    # -----------------------------------------------------------------
    # STEP 3: Sort candidate list by final score descending
    # -----------------------------------------------------------------
    candidates_results.sort(key=lambda x: x.get("final_score", 0), reverse=True)

    elapsed_time = round(time.time() - start_time, 2)

    return {
        "rubric": rubric,
        "candidates": candidates_results,
        "total_candidates": len(candidates_results),
        "pipeline_time_seconds": elapsed_time
    }
