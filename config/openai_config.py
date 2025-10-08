# config/openai_config.py
"""
Handles OpenAI API configuration and setup.
Works with local .env (optional) and Streamlit Cloud secrets.
"""

from openai import OpenAI

# Try fetching the API key
try:
    # If running on Streamlit Cloud
    import streamlit as st
    api_key = st.secrets.get("OPENAI_API_KEY")
except ImportError:
    api_key = None

# Fallback for local development using environment variable
import os
if not api_key:
    api_key = os.getenv("OPENAI_API_KEY")

# Check if the API key exists
if not api_key:
    raise ValueError(
        "OpenAI API key not found. "
        "Add it to Streamlit Secrets or as an environment variable locally."
    )

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Simple test function
def test_connection():
    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input="Test connection successful?"
        )
        print("OpenAI connection successful!")
        print("AI Response:", response.output_text)
    except Exception as e:
        print("OpenAI connection failed:", e)


if __name__ == "__main__":
    print("Testing OpenAI connection...")
    test_connection()
