"""
Anthropic Claude Client implementation for the cooking assistant.
"""

import os 
from typing import Dict, List, Optional, Any

from anthropic import Anthropic
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import HumanMessage, SystemMessage

# load environment variables
load_dotenv()

def get_claude_client() -> BaseChatModel:
    """
    Initialize and return the Claude language model client.

    Returns:
        BaseChatModel: The configured Claude language model.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")

    model_name = os.getenv("MODEL_NAME", "claude-3-5-sonnet")
    temperature = float(os.getenv("TEMPERATURE", "0.7"))
    max_tokens = int(os.getenv("MAX_TOKENS", "1024"))

    # initialize the Anthropic client with LangChain
    claude = ChatAnthropic(
        model_name=model_name,
        anthropic_api_key=api_key,
        temperature=temperature,
        max_tokens_to_sample=max_tokens,
    )

    return claude

def get_direct_client() -> Anthropic:
    """
    Get the direct Anthropic client for more advanced usage.

    Returns:
        Anthropic: The Anthropic client.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")

    return Anthropic(api_key=api_key)

def generate_response(
    ingredients: List[str], 
    dietary_restrictions: Optional[List[str]] = None,
    preferences: Optional[Dict[str, Any]] = None,
    system_prompt: Optional[str] = None,
) -> str:
    """
    Generate recipe suggestions based on ingredients.

    Args:
        ingredients: List of available ingredients
        dietary_restrictions: Optional list of dietary restrictions (e.g., "vegetarian", "gluten-free")
        preferences: Optional dict of user preferences (e.g., {"cuisine": "Italian", "difficulty": "easy"})
        system_prompt: Optional custom system prompt
        
    Returns:
        str: The generated recipe suggestion
    """
    claude = get_claude_client()

    if system_prompt is None:
        system_prompt = _create_system_prompt()

    # create the ingredients prompt
    ingredients_text = ", ".join(ingredients)
    restrictions_text = ""
    if dietary_restrictions:
        restrictions_text = f"Dietary restrictions: {', '.join(dietary_restrictions)}. "

    preferences_text = ""
    if preferences:
        pref_items = [f"{k}: {v}" for k, v in preferences.items()]
        preferences_text = f"Preferences: {', '.join(pref_items)}. "
    
    user_prompt = (
        f"I have these ingredients: {ingredients_text}. "
        f"{restrictions_text}"
        f"{preferences_text}"
        "What meal can I cook with these ingredients?"
    )
    
    # Generate response using the LangChain interface
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]
    
    response = claude.invoke(messages)
    return response.content

def _create_system_prompt() -> str:
    """
    Create the system prompt for recipe generation.
    
    Returns:
        str: The system prompt for the model.
    """
    return """You are a helpful cooking assistant that suggests meals based on available ingredients.
    
Your task is to:
1. Analyze the provided ingredients
2. Suggest a suitable meal that can be prepared with those ingredients
3. Provide a clear recipe with ingredients, measurements, and step-by-step instructions
4. Consider any dietary restrictions or preferences mentioned
5. If critical ingredients are missing, suggest simple substitutions or additions

When making suggestions:
- Be creative but practical
- Prioritize using as many of the available ingredients as possible
- Suggest common substitutes if a recipe needs additional ingredients
- Include estimated preparation and cooking time
- Format your response clearly with sections for ingredients, instructions, and tips

Keep your responses concise, practical, and easy to follow.
"""   