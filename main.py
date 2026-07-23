"""
STUDENT GUIDE - FASTAPI WEB SERVER (main.py)

What does this file do?
It creates a simple web server using FastAPI.
- Serves the dashboard web page (index.html)
- Receives Job Description text & uploaded PDF resumes from the user
- Loads environment variables from .env file automatically
- Calls `run_screening_pipeline()` and sends back candidate scores!
"""

import os
from typing import List, Optional
from fastapi import FastAPI, Request, Form, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

from services.pdf_service import extract_text_from_file
from services.pipeline import run_screening_pipeline

# Automatically load environment variables from .env file
load_dotenv()

# Initialize FastAPI App
app = FastAPI(title="Autonomous Resume Screening Agent", version="1.0.0")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))


# Web Page Dashboard Route
@app.get("/", response_class=HTMLResponse)
async def serve_dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


# Health Check Route
@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "service": "Autonomous Resume Screening Agent",
        "groq_key_configured": bool(os.getenv("GROQ_API_KEY"))
    }


# Main Screening API Route
@app.post("/api/screen")
async def screen_candidates(
    jd_text: str = Form(...),
    api_key: Optional[str] = Form(None),
    resume_files: List[UploadFile] = File(...)
):
    # Use API key from Form data or from .env environment variable
    effective_api_key = (api_key and api_key.strip()) or os.getenv("GROQ_API_KEY")
    
    if not effective_api_key:
        raise HTTPException(
            status_code=400,
            detail="GROQ_API_KEY is missing! Please set GROQ_API_KEY in your .env file or enter it in the header."
        )

    # Read uploaded resume files
    resumes_list = []
    for file in resume_files:
        if file.filename:
            contents = await file.read()
            text = extract_text_from_file(contents, file.filename)
            resumes_list.append({"filename": file.filename, "text": text})

    if not resumes_list:
        raise HTTPException(status_code=400, detail="Please upload at least one resume file.")

    # Call the 4-Agent Pipeline!
    try:
        results = run_screening_pipeline(jd_text=jd_text, resumes=resumes_list, api_key=effective_api_key)
        return results
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
