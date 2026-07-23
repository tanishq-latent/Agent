"""
STUDENT GUIDE - STEP 1: Talking to Groq AI (agents/base.py)

This file contains ONE simple helper function: `ask_groq_ai()`.
It sends your prompt to Groq AI (Llama 3.3) and returns the response as a Python dictionary.
"""

import os
import json
import re
from groq import Groq


def ask_groq_ai(system_prompt: str, user_prompt: str, api_key: str = None) -> dict:
    """Sends a system prompt and user prompt to Groq AI and returns a Python dictionary."""
    key = api_key or os.getenv("GROQ_API_KEY")
    if not key:
        raise ValueError("GROQ_API_KEY is missing! Please set it in your environment or .env file.")

    client = Groq(api_key=key)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt + "\n\nIMPORTANT: Respond strictly in valid JSON format."},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.2,
        response_format={"type": "json_object"}
    )

    raw_text = response.choices[0].message.content.strip()

    if raw_text.startswith("```json"):
        raw_text = raw_text[7:]
    if raw_text.startswith("```"):
        raw_text = raw_text[3:]
    if raw_text.endswith("```"):
        raw_text = raw_text[:-3]

    try:
        return json.loads(raw_text.strip())
    except json.JSONDecodeError:
        match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        if match:
            return json.loads(match.group(0))
        raise ValueError("Could not parse valid JSON response from AI.")
