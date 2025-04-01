"""
Model integration module for the cooking agent assistant.
"""

from .claude_client import get_claude_client, generate_response

__all__=["get_claude_client", "generate_response"]