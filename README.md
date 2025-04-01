# Cooking Assistant Agent

A LangGraph-powered cooking assistant that suggests meals based on available ingredients using Anthropic's Claude API.

## Features

- **Ingredient-Based Recipe Generation**: Get cooking suggestions based on ingredients you have available
- **Intelligent Recommendations**: Leverages Anthropic's Claude model for contextual understanding and creative recipe ideas
- **Streamlit UI**: Easy-to-use interface for ingredient input and recipe display
- **API Access**: Deployed with LangServe and FastAPI for programmatic access

## Setup

1. Clone this repository
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Copy `.env.example` to `.env` and add your Anthropic API key

## Usage

### Streamlit UI
```
streamlit run ui/app.py
```

### API Access
```
cd myserve
uvicorn app:app --reload
```

## Deployment

This project is configured for deployment using AWS Copilot. See deployment documentation for details.

## Project Structure

- `agent/`: LangGraph agent implementation
- `memory/`: Conversation memory components
- `model/`: Anthropic API integration
- `myserve/`: FastAPI and LangServe setup
- `ui/`: Streamlit user interface

## License

MIT