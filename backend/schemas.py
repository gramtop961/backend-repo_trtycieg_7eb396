from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime

# Each model corresponds to a MongoDB collection named after class lowercased

class Lead(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    phone: str = Field(..., min_length=7, max_length=20)
    email: Optional[EmailStr] = None
    service: str = Field(..., description="Requested service")
    message: Optional[str] = Field(None, max_length=2000)
    city: Optional[str] = Field(None, max_length=100)
    source: Optional[str] = Field(None, description="utm/source or page")

class ServiceArea(BaseModel):
    name: str
    slug: str
    county: Optional[str] = None
    description: Optional[str] = None

class Testimonial(BaseModel):
    name: str
    location: Optional[str] = None
    rating: int = Field(ge=1, le=5)
    content: str

class ServicePage(BaseModel):
    slug: str
    title: str
    headline: str
    intro: str
    faqs: List[dict] = []

