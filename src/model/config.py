"""
Configuration settings for model integration.
"""

import os
from typing import Dict, Any
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# load environment variables
load_dotenv()

class ModelConfig(BaseModel):
    """Configuration for the Claude model."""
    
    model_name: str = Field(
        default_factory=lambda: os.getenv("MODEL_NAME", "claude-3-5-sonnet")
    )
    temperature: float = Field(
        default_factory=lambda: float(os.getenv("TEMPERATURE", "0.7"))
    )
    max_tokens: int = Field(
        default_factory=lambda: int(os.getenv("MAX_TOKENS", "1024"))
    )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert config to dictionary."""
        return self.model_dump()

def get_model_config() -> ModelConfig:
    """
    Get the model configuration from environment variables.
    
    Returns:
        ModelConfig: The model configuration.
    """
    return ModelConfig()