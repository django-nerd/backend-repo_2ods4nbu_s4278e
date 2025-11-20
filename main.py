import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

from database import db, create_document, get_documents
from schemas import Inquiry, QuoteRequest, Testimonial, PortfolioItem

app = FastAPI(title="Boesman Creative Co. API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Boesman Creative Co. API is running"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set",
        "database_name": "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set",
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
                response["connection_status"] = "Connected"
            except Exception as e:
                response["database"] = f"⚠️ Connected but error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"

    return response

# Contact inquiry endpoint
@app.post("/api/inquiries")
def submit_inquiry(payload: Inquiry):
    try:
        inserted_id = create_document("inquiry", payload)
        return {"status": "ok", "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Quote request endpoint
@app.post("/api/quotes")
def submit_quote(payload: QuoteRequest):
    try:
        inserted_id = create_document("quoterequest", payload)
        return {"status": "ok", "id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Public fetch endpoints (simple lists)
@app.get("/api/testimonials", response_model=List[Testimonial])
def list_testimonials(limit: int = 6):
    # For demo purposes, return curated static content if DB lacks data
    try:
        docs = get_documents("testimonial", limit=limit)
        if docs:
            mapped = []
            for d in docs:
                d.pop("_id", None)
                mapped.append(Testimonial(**d))
            return mapped
    except Exception:
        pass
    # Fallback static testimonials
    return [
        Testimonial(name="Nico Boesman", role="Owner", company="Boesman Creative Co.", quote="We turn ideas into bold, tangible brand moments.", rating=5),
        Testimonial(name="Anna L.", role="Marketing Lead", company="Local FMCG Brand", quote="Reliable, fast and the print quality is excellent.", rating=5),
        Testimonial(name="Taimi N.", role="Founder", company="Startup Namibia", quote="They nailed our signage and merch on a tight deadline.", rating=5),
    ]

@app.get("/api/portfolio", response_model=List[PortfolioItem])
def list_portfolio(limit: int = 12):
    try:
        docs = get_documents("portfolioitem", limit=limit)
        if docs:
            items = []
            for d in docs:
                d.pop("_id", None)
                items.append(PortfolioItem(**d))
            return items
    except Exception:
        pass
    # Fallback static sample
    samples = [
        PortfolioItem(title="Brand Roll-up Banners", image_url="https://images.unsplash.com/photo-1520975661595-6453be3f7070?q=80&w=1600&auto=format&fit=crop", category="Large Format"),
        PortfolioItem(title="DTF Printed Tees", image_url="https://images.unsplash.com/photo-1520975661595-6453be3f7070?q=80&w=1200&auto=format&fit=crop", category="DTF"),
        PortfolioItem(title="Outdoor Signage", image_url="https://images.unsplash.com/photo-1531973968078-9bb02785f13d?q=80&w=1600&auto=format&fit=crop", category="Signage"),
        PortfolioItem(title="Corporate Wear", image_url="https://images.unsplash.com/photo-1520975661595-6453be3f7070?q=80&w=1200&auto=format&fit=crop", category="Apparel"),
        PortfolioItem(title="Embroidery Caps", image_url="https://images.unsplash.com/photo-1521572267360-ee0c2909d518?q=80&w=1200&auto=format&fit=crop", category="Embroidery"),
        PortfolioItem(title="Custom Gifts", image_url="https://images.unsplash.com/photo-1512428559087-560fa5ceab42?q=80&w=1600&auto=format&fit=crop", category="Gifts"),
    ]
    return samples

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
