"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogpost" collection
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List

# Marketing site data models

class Inquiry(BaseModel):
    """General contact inquiries from the website"""
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=30)
    company: Optional[str] = Field(None, max_length=120)
    subject: Optional[str] = Field(None, max_length=150)
    message: str = Field(..., min_length=5, max_length=2000)
    source: Optional[str] = Field("contact", description="Form source identifier")

class QuoteRequest(BaseModel):
    """Detailed quote requests for printing/branding services"""
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=30)
    company: Optional[str] = Field(None, max_length=120)
    service: str = Field(..., description="Requested service type")
    quantity: Optional[int] = Field(None, ge=1, le=100000)
    size: Optional[str] = Field(None, max_length=60, description="Dimensions or sizes")
    colors: Optional[str] = Field(None, max_length=120)
    deadline: Optional[str] = Field(None, max_length=60)
    details: Optional[str] = Field(None, max_length=3000)
    source: Optional[str] = Field("quote", description="Form source identifier")

class Testimonial(BaseModel):
    name: str
    role: Optional[str] = None
    company: Optional[str] = None
    quote: str
    rating: Optional[int] = Field(5, ge=1, le=5)

class PortfolioItem(BaseModel):
    title: str
    image_url: str
    category: Optional[str] = None
    client: Optional[str] = None
    description: Optional[str] = None
