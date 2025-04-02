"""
Test script for the cooking agent.

Run this to test if your agent is working correctly.
"""

import sys
import os
from pprint import pprint

# Add the project root to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.cooking_agent import run_agent


def test_cooking_agent():
    """Test the cooking agent with sample inputs."""
    
    print("Testing the cooking agent...")
    
    # Sample test data
    ingredients = ["chicken breast", "potatoes", "broccoli", "garlic", "lemon", "olive oil"]
    dietary_restrictions = ["dairy-free"]
    preferences = {"cuisine": "Mediterranean", "difficulty": "easy"}
    query = "I'd like a healthy dinner option that's not too time-consuming."
    
    try:
        # Run the agent
        result = run_agent(
            ingredients=ingredients,
            dietary_restrictions=dietary_restrictions,
            preferences=preferences,
            query=query
        )
        
        print("\n=== Successfully ran the cooking agent ===\n")
        
        # The result might be in a different format than expected
        # Check what type of result we're getting
        print(f"Result type: {type(result)}")
        
        # Try different ways to access the result
        if hasattr(result, 'get'):
            # If result is dict-like
            recipe_name = result.get('recipe_name', 'Unknown Recipe')
            cooking_time = result.get('cooking_time', 'Unknown')
            difficulty = result.get('difficulty', 'Unknown')
            ingredients_used = result.get('ingredients_used', [])
            missing_ingredients = result.get('missing_ingredients', [])
            recipe_content = result.get('recipe_content', '')
        else:
            # Try accessing as object attributes
            recipe_name = getattr(result, 'recipe_name', 'Unknown Recipe')
            cooking_time = getattr(result, 'cooking_time', 'Unknown')
            difficulty = getattr(result, 'difficulty', 'Unknown')
            ingredients_used = getattr(result, 'ingredients_used', [])
            missing_ingredients = getattr(result, 'missing_ingredients', [])
            recipe_content = getattr(result, 'recipe_content', '')
        
        print(f"Recipe: {recipe_name}")
        print(f"Cooking Time: {cooking_time}")
        print(f"Difficulty: {difficulty}")
        
        print("\nIngredients Used:")
        for ingredient in ingredients_used:
            print(f"- {ingredient}")
            
        if missing_ingredients:
            print("\nAdditional Ingredients Recommended:")
            for ingredient in missing_ingredients:
                print(f"- {ingredient}")
        
        print("\nRecipe:")
        print(recipe_content)
        
        return True
        
    except Exception as e:
        print("\n=== Error running the cooking agent ===\n")
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    test_cooking_agent()