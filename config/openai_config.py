# config/openai_config.py
"""
Handles OpenAI API configuration and setup.
Compatible with both local .env and Streamlit Cloud secrets.
"""

import os
from openai import OpenAI

# Optionally use dotenv locally
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not needed on Streamlit Cloud

# Try fetching the API key from environment or Streamlit secrets
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    try:
        import streamlit as st
        api_key = st.secrets["OPENAI_API_KEY"]
    except (ImportError, KeyError):
        raise ValueError(
            "OpenAI API key not found. "
            "Add it to a .env file locally or to Streamlit secrets."
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
