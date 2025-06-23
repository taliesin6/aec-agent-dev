# src/check_models.py
import vertexai
from vertexai.preview.generative_models import GenerativeModel
import os
from dotenv import load_dotenv

load_dotenv()

def list_available_models():
    """Check what Gemini models are available"""
    project_id = os.getenv("PROJECT_ID")
    vertexai.init(project=project_id, location="us-central1")
    
    # Try different model names that might be available
    models_to_try = [
        "gemini-1.5-flash",
        "gemini-1.5-pro",
        "gemini-pro",
        "gemini-pro-vision"
    ]
    
    for model_name in models_to_try:
        try:
            model = GenerativeModel(model_name)
            print(f"✅ {model_name} - Available")
        except Exception as e:
            print(f"❌ {model_name} - Error: {str(e)[:100]}...")

if __name__ == "__main__":
    list_available_models()