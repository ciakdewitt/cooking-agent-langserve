"""
Test script for the model integration.

Run this to test if your Claude API integration is working correctly.
"""

import sys
import os

# Add the project root to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from model.claude_client import generate_response

def test_claude_integration():
    """Test the Claude API integration with a simple query."""
    
    print("Testing Claude API integration...")
    
    # Sample ingredients for testing
    ingredients = ["chicken breast", "rice", "onion", "bell pepper", "garlic", "olive oil"]
    dietary_restrictions = ["dairy-free"]
    preferences = {"cuisine": "Mediterranean", "difficulty": "easy"}
    
    try:
        response = generate_response(
            ingredients=ingredients,
            dietary_restrictions=dietary_restrictions,
            preferences=preferences
        )
        
        print("\n--- Successfully connected to Claude API ---\n")
        print("Ingredients:", ", ".join(ingredients))
        print("\nGenerated Response:\n")
        print(response)
        return True
        
    except Exception as e:
        print(f"\n--- Error connecting to Claude API ---\n")
        print(f"Error: {str(e)}")
        print("\nMake sure your ANTHROPIC_API_KEY is correctly set in the .env file.")
        return False

if __name__ == "__main__":
    test_claude_integration()