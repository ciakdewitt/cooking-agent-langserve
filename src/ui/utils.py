"""
Utility functions for the Streamlit UI.
"""

import random
from typing import List, Dict, Any

# List of common ingredient combinations for quick selection
INGREDIENT_COMBOS = [
    {
        "name": "Italian Night",
        "ingredients": ["Pasta", "Tomato", "Garlic", "Onion", "Olive Oil", "Basil", "Parmesan"]
    },
    {
        "name": "Mexican Fiesta",
        "ingredients": ["Tortillas", "Bell Pepper", "Onion", "Black Beans", "Rice", "Lime", "Cilantro"]
    },
    {
        "name": "Asian Stir Fry",
        "ingredients": ["Rice", "Bell Pepper", "Broccoli", "Carrot", "Soy Sauce", "Garlic", "Ginger"]
    },
    {
        "name": "Breakfast",
        "ingredients": ["Eggs", "Bread", "Cheese", "Spinach", "Tomato", "Butter"]
    },
    {
        "name": "Comfort Food",
        "ingredients": ["Potato", "Butter", "Cheese", "Milk", "Garlic", "Onion"]
    }
]


def get_random_ingredients(count: int = 5) -> List[str]:
    """
    Get a random selection of ingredients.
    
    Args:
        count: Number of random ingredients to select
        
    Returns:
        List of randomly selected ingredients
    """
    all_ingredients = []
    for category_ingredients in INGREDIENT_CATEGORIES.values():
        all_ingredients.extend(category_ingredients)
    
    # Ensure we don't request more ingredients than available
    count = min(count, len(all_ingredients))
    
    return random.sample(all_ingredients, count)


def format_recipe_output(recipe_content: str) -> str:
    """
    Format the raw recipe content for better display.
    
    Args:
        recipe_content: Raw recipe content from the agent
        
    Returns:
        Formatted recipe content for display
    """
    # This could be expanded to do more sophisticated formatting
    # Currently just returning the raw content
    return recipe_content


# Categorized ingredients for organized display
INGREDIENT_CATEGORIES = {
    "Proteins": [
        "Chicken", "Beef", "Pork", "Fish", "Tofu", "Eggs", 
        "Beans", "Lentils", "Chickpeas", "Tempeh"
    ],
    "Vegetables": [
        "Tomato", "Onion", "Garlic", "Bell Pepper", "Carrot",
        "Spinach", "Broccoli", "Potato", "Corn", "Mushroom"
    ],
    "Grains": [
        "Rice", "Pasta", "Bread", "Quinoa", "Oats",
        "Flour", "Couscous", "Tortilla", "Noodles"
    ],
    "Dairy": [
        "Milk", "Cheese", "Butter", "Yogurt", "Cream"
    ],
    "Herbs & Spices": [
        "Salt", "Pepper", "Basil", "Oregano", "Cilantro",
        "Cumin", "Paprika", "Cinnamon", "Thyme", "Rosemary"
    ],
    "Condiments": [
        "Olive Oil", "Soy Sauce", "Vinegar", "Mayonnaise",
        "Ketchup", "Mustard", "Honey", "Hot Sauce"
    ]
}