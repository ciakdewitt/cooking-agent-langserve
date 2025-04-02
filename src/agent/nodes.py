"""
Node definitions for the cooking agent's workflow.
"""

import os
from typing import Dict, List, Tuple, Any, Optional

from langchain_core.messages import HumanMessage, SystemMessage

from model.claude_client import get_claude_client
from .schema import AgentState, ParsedIngredients, RecipeIdea, AgentOutput

def parse_ingredients(state: AgentState) -> AgentState:
    """
    Parse and categorized ingredients from user input.

    Args:
        state: current agent state

    Returns:
        Updated agent state with parsed ingredients
    """
    claude = get_claude_client()

    ingredients_text = ", ".join(state.input.ingredients)

    system_prompt = """You are an expert chef analyzing a list of ingredients. 
    Categorize these ingredients into:
    1. Proteins (meat, fish, tofu, legumes, etc.)
    2. Vegetables and fruits
    3. Grains and starches (rice, pasta, potatoes, etc.)
    4. Seasonings (herbs, spices, oils, etc.)
    
    Also identify any common essentials that might be missing but are typically assumed to be in a kitchen (salt, pepper, common spices).
    Format your response as JSON matching the ParsedIngredients schema.
    """
    
    user_prompt = f"Here are my ingredients: {ingredients_text}"
    if state.input.dietary_restrictions:
        restrictions = ", ".join(state.input.dietary_restrictions)
        user_prompt += f"\nI have these dietary restrictions: {restrictions}"
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]
    
    response = claude.invoke(messages)
    
    # Parse the JSON response
    try:
        import json
        # Extract JSON from response
        json_content = response.content
        # If JSON is embedded in markdown, extract it
        if "```json" in json_content:
            json_content = json_content.split("```json")[1].split("```")[0].strip()
        elif "```" in json_content:
            json_content = json_content.split("```")[1].split("```")[0].strip()
        
        parsed_data = json.loads(json_content)
        
        # Create ParsedIngredients from the parsed data
        parsed_ingredients = ParsedIngredients(
            main_ingredients=state.input.ingredients,
            proteins=parsed_data.get("proteins", []),
            vegetables=parsed_data.get("vegetables", []),
            grains=parsed_data.get("grains", []),
            seasonings=parsed_data.get("seasonings", []),
            missing_essentials=parsed_data.get("missing_essentials", [])
        )
        
        # Update state
        state.parsed_ingredients = parsed_ingredients
        
    except Exception as e:
        # Fallback if JSON parsing fails
        state.parsed_ingredients = ParsedIngredients(
            main_ingredients=state.input.ingredients,
            proteins=[],
            vegetables=[],
            grains=[],
            seasonings=[],
            missing_essentials=[]
        )
    
    return state  

def generate_recipe_idea(state: AgentState) -> AgentState:
    """
    Generate recipe ideas based on parsed ingredients.
    
    Args:
        state: Current agent state with parsed ingredients
        
    Returns:
        Updated agent state with recipe idea
    """
    claude = get_claude_client()
    
    if not state.parsed_ingredients:
        # Fallback if ingredients haven't been parsed
        state = parse_ingredients(state)
    
    # Create formatted ingredient lists
    all_ingredients = state.input.ingredients
    proteins = state.parsed_ingredients.proteins
    vegetables = state.parsed_ingredients.vegetables
    grains = state.parsed_ingredients.grains
    
    system_prompt = """You are a creative chef who specializes in creating recipe ideas from available ingredients.
    Based on the ingredients provided, suggest a suitable recipe concept.
    Consider dietary restrictions and preferences if provided.
    Format your response as JSON that matches the RecipeIdea schema.
    """
    
    user_prompt = f"Available ingredients: {', '.join(all_ingredients)}\n"
    
    if proteins:
        user_prompt += f"Proteins: {', '.join(proteins)}\n"
    if vegetables:
        user_prompt += f"Vegetables: {', '.join(vegetables)}\n"
    if grains:
        user_prompt += f"Grains/Starches: {', '.join(grains)}\n"
    
    if state.input.dietary_restrictions:
        user_prompt += f"Dietary restrictions: {', '.join(state.input.dietary_restrictions)}\n"
    
    if state.input.preferences:
        preferences_text = ", ".join([f"{k}: {v}" for k, v in state.input.preferences.items()])
        user_prompt += f"Preferences: {preferences_text}\n"
    
    user_prompt += "\nSuggest a creative recipe idea that uses these ingredients efficiently."
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]
    
    response = claude.invoke(messages)
    
    # Parse the JSON response
    try:
        import json
        # Extract JSON from response
        json_content = response.content
        # If JSON is embedded in markdown, extract it
        if "```json" in json_content:
            json_content = json_content.split("```json")[1].split("```")[0].strip()
        elif "```" in json_content:
            json_content = json_content.split("```")[1].split("```")[0].strip()
        
        parsed_data = json.loads(json_content)
        
        # Create RecipeIdea from the parsed data
        recipe_idea = RecipeIdea(
            name=parsed_data.get("name", "Custom Recipe"),
            cuisine_type=parsed_data.get("cuisine_type", "Fusion"),
            difficulty=parsed_data.get("difficulty", "medium"),
            cooking_time=parsed_data.get("cooking_time", "30 minutes"),
            suitable_for_restrictions=parsed_data.get("suitable_for_restrictions", True)
        )
        
        # Update state
        state.recipe_idea = recipe_idea
        
    except Exception as e:
        # Fallback if JSON parsing fails
        state.recipe_idea = RecipeIdea(
            name="Custom Recipe",
            cuisine_type="Fusion",
            difficulty="medium",
            cooking_time="30 minutes",
            suitable_for_restrictions=True
        )
    
    return state


def create_full_recipe(state: AgentState) -> AgentState:
    """
    Create a detailed recipe based on the recipe idea and ingredients.
    
    Args:
        state: Current agent state with recipe idea
        
    Returns:
        Updated agent state with full recipe content
    """
    claude = get_claude_client()
    
    if not state.recipe_idea:
        # Generate recipe idea if not already done
        state = generate_recipe_idea(state)
    
    system_prompt = """You are a professional chef creating detailed recipes.
    Create a complete recipe with ingredients list, measurements, and step-by-step instructions.
    The recipe should be practical, detailed, and easy to follow.
    Format the recipe clearly with sections for Ingredients, Instructions, and Cooking Tips.
    """
    
    user_prompt = f"Recipe: {state.recipe_idea.name}\n"
    user_prompt += f"Cuisine: {state.recipe_idea.cuisine_type}\n"
    user_prompt += f"Difficulty: {state.recipe_idea.difficulty}\n"
    user_prompt += f"Available ingredients: {', '.join(state.input.ingredients)}\n"
    
    if state.parsed_ingredients.missing_essentials:
        user_prompt += f"Assumed kitchen staples: {', '.join(state.parsed_ingredients.missing_essentials)}\n"
    
    if state.input.dietary_restrictions:
        user_prompt += f"Dietary restrictions: {', '.join(state.input.dietary_restrictions)}\n"
    
    if state.input.query:
        user_prompt += f"Additional requirements: {state.input.query}\n"
    
    user_prompt += "\nPlease create a complete recipe with measurements and detailed instructions."
    
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]
    
    response = claude.invoke(messages)
    
    # Update state with the recipe content
    state.recipe_content = response.content
    
    return state


def prepare_output(state: AgentState) -> AgentOutput:
    """
    Prepare the final output from the agent state.
    
    Args:
        state: Final agent state with recipe content
        
    Returns:
        Formatted agent output
    """
        
    # Ensure we have all necessary components
    if not state.recipe_content:
        state = create_full_recipe(state)
    
    if not state.recipe_idea:
        state = generate_recipe_idea(state)
    
    # Create the output
    output = AgentOutput(
        recipe_name=state.recipe_idea.name,
        ingredients_used=state.input.ingredients,
        recipe_content=state.recipe_content,
        cooking_time=state.recipe_idea.cooking_time,
        difficulty=state.recipe_idea.difficulty,
        missing_ingredients=state.parsed_ingredients.missing_essentials if state.parsed_ingredients else []
    )
    
    return output