# config/openai_config.py
"""
Handles OpenAI API configuration and setup.
Keeps your API key loading separate for cleaner, modular code.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Fetch the API key
api_key = os.getenv("OPENAI_API_KEY")

# Ensure API key is found
if not api_key:
    raise ValueError("❌ OpenAI API key not found. Please add it to your .env file.")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Simple test function to check connection
def test_connection():
    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input="Test connection successful?"
        )
        print("✅ OpenAI connection successful!")
        print("AI Response:", response.output_text)
    except Exception as e:
        print("❌ OpenAI connection failed:", e)

# 👇 Add this block to actually run the test
if __name__ == "__main__":
    print("🔍 Testing OpenAI connection...")
    test_connection()
