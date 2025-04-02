"""
FastAPI application for the cooking assistant API.
"""

import os
import sys
from typing import List, Dict, Optional, Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Add the project root to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.cooking_agent import run_agent

# Create FastAPI app
app = FastAPI(
    title="Cooking Assistant API",
    description="Generate recipe suggestions based on available ingredients",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define input/output models for the API
class CookingAssistantInput(BaseModel):
    """Input model for the cooking assistant API."""
    
    ingredients: List[str] = Field(
        description="List of available ingredients",
        examples=[["chicken", "rice", "onion", "olive oil"]]
    )
    dietary_restrictions: Optional[List[str]] = Field(
        default_factory=list,
        description="Optional list of dietary restrictions",
        examples=[["vegetarian", "gluten-free"]]
    )
    preferences: Optional[Dict[str, Any]] = Field(
        default_factory=dict,
        description="Optional dictionary of preferences",
        examples=[{"cuisine": "Italian", "difficulty": "easy"}]
    )
    query: Optional[str] = Field(
        default=None,
        description="Additional instructions or requirements for the recipe"
    )


class CookingAssistantOutput(BaseModel):
    """Output model for the cooking assistant API."""
    
    recipe_name: str = Field(description="Name of the suggested recipe")
    ingredients_used: List[str] = Field(description="List of ingredients used in the recipe")
    recipe_content: str = Field(description="The full recipe with instructions")
    cooking_time: str = Field(description="Estimated cooking time")
    difficulty: str = Field(description="Difficulty level of the recipe")
    missing_ingredients: List[str] = Field(
        default_factory=list,
        description="Any ingredients that would be nice to have but weren't in the input"
    )


@app.post("/api/recipe", response_model=CookingAssistantOutput)
async def generate_recipe(input_data: CookingAssistantInput):
    """
    Generate a recipe based on the provided ingredients and preferences.
    
    Args:
        input_data: The input data containing ingredients and preferences
        
    Returns:
        The generated recipe and related information
    """
    try:
        # Call the agent
        result = run_agent(
            ingredients=input_data.ingredients,
            dietary_restrictions=input_data.dietary_restrictions,
            preferences=input_data.preferences,
            query=input_data.query
        )
        
        # Process the result
        # Since our agent returns a LangGraph structure, we need to extract the data
        if hasattr(result, 'get'):
            # Dict-like access
            recipe_name = result.get('recipe_name', 'Custom Recipe')
            recipe_content = result.get('recipe_content', '')
            cooking_time = result.get('cooking_time', 'Not specified')
            difficulty = result.get('difficulty', 'Not specified')
            missing_ingredients = result.get('missing_ingredients', [])
        else:
            # Attribute access
            recipe_name = getattr(result, 'recipe_name', 'Custom Recipe')
            recipe_content = getattr(result, 'recipe_content', '')
            cooking_time = getattr(result, 'cooking_time', 'Not specified')
            difficulty = getattr(result, 'difficulty', 'Not specified')
            missing_ingredients = getattr(result, 'missing_ingredients', [])
        
        # Create the output
        output = CookingAssistantOutput(
            recipe_name=recipe_name,
            ingredients_used=input_data.ingredients,
            recipe_content=recipe_content,
            cooking_time=cooking_time,
            difficulty=difficulty,
            missing_ingredients=missing_ingredients
        )
        
        return output
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating recipe: {str(e)}")


# Add a basic health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# Root endpoint with API information
@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "name": "Cooking Assistant API",
        "version": app.version,
        "description": app.description,
        "endpoints": {
            "/api/recipe": "Generate recipe suggestions",
            "/health": "Health check endpoint",
            "/docs": "API documentation (Swagger UI)",
            "/redoc": "API documentation (ReDoc)"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)