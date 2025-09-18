from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from typing import List, Dict, Any

from services.llm_service import LLMService
from services.product_service import ProductService

app = FastAPI(title="AI Product Recommendation API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
product_service = ProductService()
llm_service = LLMService()

# Request models
class UserPreferences(BaseModel):
    priceRange: str = "all"
    categories: List[str] = []
    brands: List[str] = []

class RecommendationRequest(BaseModel):
    preferences: UserPreferences
    browsing_history: List[str] = []


@app.get("/api/products")
async def get_products():
    """
    Return the full product catalog
    """
    products = product_service.get_all_products()
    return products

@app.post("/api/recommendations")
async def get_recommendations(request: RecommendationRequest):
    """
    Generate personalized product recommendations using Gemini
    """
    try:
        user_preferences = request.preferences.dict()
        browsing_history = request.browsing_history

        recommendations = llm_service.generate_recommendations(
            user_preferences,
            browsing_history,
            product_service.get_all_products()
        )
        return recommendations

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return {
        "error": str(exc),
        "message": "An error occurred while processing your request"
    }

@app.get("/")
def root():
    return {"message": "Welcome to the Product Recommendation API. Visit /docs for API documentation."}


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)