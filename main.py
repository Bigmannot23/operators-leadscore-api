from fastapi import FastAPI, Request, Header, HTTPException, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr, HttpUrl, ValidationError
from typing import Optional, Set
from pathlib import Path
import datetime

app = FastAPI(
    title="OperatorOS Lead Scoring API",
    version="1.0.0",
    description="Compounding, operator-ready lead scoring with API key authentication."
)

# --- MAX MODE: API Key Loader ---
def load_api_keys(filename: str = "api_keys.txt") -> Set[str]:
    """Load API keys from a plaintext file, one per line."""
    path = Path(filename)
    if not path.exists():
        print(f"WARNING: {filename} not found. No API keys loaded.")
        return set()
    with path.open("r") as f:
        # Strips whitespace, skips blank lines and comments
        return {line.strip() for line in f if line.strip() and not line.startswith("#")}

API_KEYS = load_api_keys()

# --- MAX MODE: Dependency for API Key Auth ---
async def api_key_auth(x_api_key: Optional[str] = Header(None)):
    """
    Require a valid API key in 'X-API-Key' header.
    """
    if not API_KEYS:
        raise HTTPException(status_code=500, detail="API key system misconfigured: no keys loaded.")
    if not x_api_key or x_api_key not in API_KEYS:
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid API key. Add 'X-API-Key' header with your assigned key."
        )
    return x_api_key

# --- Request Model ---
class Lead(BaseModel):
    name: str
    email: EmailStr
    company: Optional[str] = ""
    website: Optional[HttpUrl] = None
    industry: Optional[str] = None
    employees: Optional[int] = None

# --- Scoring Logic ---
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

# --- Lead Scoring Endpoint (MAX MODE: Auth enforced) ---
@app.post("/score_lead", response_class=JSONResponse, tags=["Scoring"])
async def score_lead(
    lead: Lead,
    request: Request,
    api_key: str = Depends(api_key_auth)
):
    """
    Score a B2B SaaS lead for pipeline qualification. Requires valid API key in X-API-Key header.
    Returns score (0-100) and breakdown.
    """
    timestamp = datetime.datetime.utcnow().isoformat()
    client_ip = request.client.host
    print(f"[{timestamp}] Scoring request: {lead.dict()} from {client_ip} | API key: {api_key}")

    scoring = score_lead_logic(lead)

    # (Optional) Add analytics, DB log, or webhook trigger here

    return {
        "lead": lead.dict(),
        "score": scoring["score"],
        "explanation": scoring["explanation"],
        "timestamp": timestamp,
        "operatoros_version": app.version
    }

# --- Root Endpoint ---
@app.get("/")
async def root():
    return {"message": "OperatorOS Lead Scoring API Live"}

# --- Input Validation Error Handler (MAX MODE) ---
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors(), "body": exc.body},
    )
# --- Run with: uvicorn main:app --reload ---
# --- Test with: curl -X POST "http://localhost:8000/score_le   

