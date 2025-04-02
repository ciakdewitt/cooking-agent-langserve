# Cooking Assistant Streamlit UI

This directory contains the Streamlit user interface for the Cooking Assistant application.

## Features

- Interactive ingredient selection by category
- Dietary restriction and preference settings
- Recipe generation using the LangGraph agent

## Running the UI

From the project root, run:

```bash
streamlit run ui/app.py
```

## Files

- `app.py`: Main Streamlit application
- `utils.py`: Helper functions and data
- `.streamlit/config.toml`: Streamlit configuration

## UI Structure

1. **Ingredient Selection**: Users can select ingredients from categorized lists or add custom ingredients
2. **Preferences Panel**: Set dietary restrictions, cuisine preferences, and difficulty level
3. **Recipe Display**: View the generated recipe with cooking instructions

## Customization

To add more ingredients or categories, edit the `INGREDIENTS` dictionary in `app.py`.