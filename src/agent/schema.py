"""
Schema definitions for the cooking agent.
"""

from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field


class AgentInput(BaseModel):
    """Input schema for the cooking agent."""
    
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


class ParsedIngredients(BaseModel):
    """Parsed ingredient information."""
    
    main_ingredients: List[str] = Field(
        description="The main ingredients identified from user input"
    )
    proteins: List[str] = Field(
        default_factory=list,
        description="Protein ingredients identified"
    )
    vegetables: List[str] = Field(
        default_factory=list,
        description="Vegetable ingredients identified"
    )
    grains: List[str] = Field(
        default_factory=list,
        description="Grain and starch ingredients identified"
    )
    seasonings: List[str] = Field(
        default_factory=list,
        description="Seasonings, herbs, and spices identified"
    )
    missing_essentials: List[str] = Field(
        default_factory=list,
        description="Essential ingredients that might be missing but commonly assumed in kitchens"
    )


class RecipeIdea(BaseModel):
    """Recipe idea generated based on ingredients."""
    
    name: str = Field(description="Name of the recipe")
    cuisine_type: str = Field(description="Type of cuisine for the recipe")
    difficulty: str = Field(description="Difficulty level (easy, medium, hard)")
    cooking_time: str = Field(description="Estimated cooking time")
    suitable_for_restrictions: bool = Field(
        description="Whether the recipe is suitable for the given dietary restrictions"
    )


class AgentState(BaseModel):
    """State maintained throughout the agent's execution."""
    
    input: AgentInput
    parsed_ingredients: Optional[ParsedIngredients] = None
    recipe_idea: Optional[RecipeIdea] = None
    recipe_content: Optional[str] = None


class AgentOutput(BaseModel):
    """Output schema for the cooking agent."""
    
    recipe_name: str = Field(description="Name of the suggested recipe")
    ingredients_used: List[str] = Field(description="List of ingredients used in the recipe")
    recipe_content: str = Field(description="The full recipe with instructions")
    cooking_time: str = Field(description="Estimated cooking time")
    difficulty: str = Field(description="Difficulty level of the recipe")
    missing_ingredients: List[str] = Field(
        default_factory=list,
        description="Any ingredients that would be nice to have but weren't in the input"
    )