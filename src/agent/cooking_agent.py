"""
Main agent implementation using LangGraph.
"""

from typing import Dict, List, Any, Optional, Annotated
import os

from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from .schema import AgentState, AgentInput, AgentOutput
from .nodes import parse_ingredients, generate_recipe_idea, create_full_recipe, prepare_output

def create_agent() -> StateGraph:
    """
    Create the cooking agent workflow graph.

    Returns:
        StateGraph: The LangGraph workflow for the cooking agent.
    """
    # create a new graph
    workflow = StateGraph(AgentState)

    # add nodes to the graph
    workflow.add_node("parse_ingredients", parse_ingredients)
    workflow.add_node("generate_recipe_idea", generate_recipe_idea)
    workflow.add_node("create_full_recipe", create_full_recipe)
    workflow.add_node("prepare_output", prepare_output)

    # define the edges in the graph
    workflow.add_edge("parse_ingredients", "generate_recipe_idea")
    workflow.add_edge("generate_recipe_idea", "create_full_recipe")
    workflow.add_edge("create_full_recipe", "prepare_output")
    workflow.add_edge("prepare_output", END)

    # set the entry point
    workflow.set_entry_point("parse_ingredients")

    # compile the graph
    return workflow.compile()

def run_agent(
    ingredients: List[str],
    dietary_restrictions: Optional[List[str]] = None,
    preferences: Optional[Dict[str, Any]] = None,
    query: Optional[str] = None
) -> AgentOutput:
    """
    Run the cooking agent with the given inputs.
    
    Args:
        ingredients: List of available ingredients
        dietary_restrictions: Optional dietary restrictions
        preferences: Optional user preferences
        query: Optional additional query or instructions
        
    Returns:
        AgentOutput: The generated recipe and related information
    """
    # Create the agent graph
    agent = create_agent()
    
    # Create the input state
    input_data = AgentInput(
        ingredients=ingredients,
        dietary_restrictions=dietary_restrictions,
        preferences=preferences,
        query=query
    )
    
    state = AgentState(input=input_data)
    
    # Run the agent
    result = agent.invoke(state)
    
    # Return the output
    return result