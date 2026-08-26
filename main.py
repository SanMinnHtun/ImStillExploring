# Run the development server from this directory with:
# uvicorn main.py --reload

from typing import Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from career_advisor.questionnaire import calculate_results
from career_advisor.resource_analyzer import analyze_and_curate_roadmap


class QuestionnaireSubmission(BaseModel):
    answers: Dict[str, str]


app = FastAPI(title="Career Advisor API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def healthcheck():
    return {"status": "ok"}


@app.post("/api/diagnose")
def diagnose(submission: QuestionnaireSubmission):
    try:
        return calculate_results(submission.answers)
    except ValueError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
