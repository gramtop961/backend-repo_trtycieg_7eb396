from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from database import create_document, get_documents
from schemas import Lead
import os

app = FastAPI(title="Franks Plumbing API", version="1.0.0")

# CORS for frontend
FRONTEND_URL = os.getenv("FRONTEND_URL", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL, "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class LeadResponse(BaseModel):
    id: str
    message: str

@app.get("/")
async def root():
    return {"message": "Backend is running"}

@app.get("/test")
async def test_db():
    # return some info about database connectivity
    try:
        collections = [doc.get("name") for doc in await get_documents("servicearea", {}, 1)]
        return {
            "backend": "ok",
            "database": "mongodb",
            "database_url": os.getenv("DATABASE_URL", "mongodb://localhost:27017"),
            "database_name": os.getenv("DATABASE_NAME", "app_db"),
            "connection_status": "connected (lazy)",
            "collections": collections,
        }
    except Exception as e:
        return {"backend": "ok", "database": "mongodb", "connection_status": f"error: {str(e)}"}

@app.post("/leads", response_model=LeadResponse)
async def submit_lead(lead: Lead):
    try:
        lead_id = await create_document("lead", lead.model_dump())
        return {"id": lead_id, "message": "Thanks! We'll reach out shortly."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Simple SEO content endpoints (optional for frontend to fetch structured data)
class Location(BaseModel):
    slug: str
    name: str
    county: Optional[str] = None

LOCATIONS: List[Location] = [
    Location(slug="fontana", name="Fontana", county="San Bernardino"),
    Location(slug="rancho-cucamonga", name="Rancho Cucamonga", county="San Bernardino"),
    Location(slug="ontario", name="Ontario", county="San Bernardino"),
    Location(slug="upland", name="Upland", county="San Bernardino"),
    Location(slug="rialto", name="Rialto", county="San Bernardino"),
    Location(slug="san-bernardino", name="San Bernardino", county="San Bernardino"),
    Location(slug="redlands", name="Redlands", county="San Bernardino"),
    Location(slug="colton", name="Colton", county="San Bernardino"),
    Location(slug="corona", name="Corona", county="Riverside"),
    Location(slug="riverside", name="Riverside", county="Riverside"),
    Location(slug="eastvale", name="Eastvale", county="Riverside"),
    Location(slug="norco", name="Norco", county="Riverside"),
    Location(slug="jurupa-valley", name="Jurupa Valley", county="Riverside"),
    Location(slug="chino", name="Chino", county="San Bernardino"),
    Location(slug="chino-hills", name="Chino Hills", county="San Bernardino"),
    Location(slug="yucaipa", name="Yucaipa", county="San Bernardino"),
]

@app.get("/locations", response_model=List[Location])
async def list_locations():
    return LOCATIONS
