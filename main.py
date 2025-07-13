from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, HttpUrl, ValidationError
from typing import Optional
import datetime

app = FastAPI()

# Request model
class Lead(BaseModel):
    name: str
    email: EmailStr
    company: Optional[str] = ""
    website: Optional[HttpUrl] = None
    industry: Optional[str] = None
    employees: Optional[int] = None

# Helper scoring function (can be upgraded to ML)
def score_lead_logic(lead: Lead) -> dict:
    score = 40  # base score
    explanation = []
    if lead.company and len(lead.company) > 2:
        score += 15
        explanation.append("Company provided (+15)")
    if lead.website:
        score += 10
        explanation.append("Website provided (+10)")
    if lead.industry:
        score += 8
        explanation.append("Industry provided (+8)")
    if lead.employees:
        if lead.employees > 50:
            score += 12
            explanation.append("Company has >50 employees (+12)")
        else:
            score += 4
            explanation.append("Small company (+4)")
    if "demo" in (lead.name.lower() + lead.email.lower()):
        score -= 20
        explanation.append("Demo/test lead detected (-20)")
    return {
        "score": min(score, 100),
        "explanation": explanation,
    }

@app.post("/score_lead", response_class=JSONResponse, tags=["Scoring"])
async def score_lead(lead: Lead, request: Request):
    """
    Score a B2B SaaS lead for pipeline qualification.
    Returns score (0-100) and breakdown.
    """
    # Timestamp and request log (for demo, prints; for prod, write to DB/file)
    timestamp = datetime.datetime.utcnow().isoformat()
    print(f"[{timestamp}] Scoring request: {lead.dict()} from {request.client.host}")

    # Calculate score and breakdown
    scoring = score_lead_logic(lead)

    # Optionally: Log results, push to analytics, or call webhook here

    return {
        "lead": lead.dict(),
        "score": scoring["score"],
        "explanation": scoring["explanation"],
        "timestamp": timestamp,
        "operatoros_version": "1.0.0"
    }

@app.get("/")
async def root():
    return {"message": "OperatorOS Lead Scoring API Live"}

# Global error handler for input validation (makes your API extra pro)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )

