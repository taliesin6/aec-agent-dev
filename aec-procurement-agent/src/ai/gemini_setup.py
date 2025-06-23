# src/ai/gemini_setup.py
import vertexai
from vertexai.generative_models import GenerativeModel
import os
from dotenv import load_dotenv

load_dotenv()

def initialize_gemini():
    """Initialize Gemini for enterprise use via Vertex AI [2][3]"""
    project_id = os.getenv("PROJECT_ID")
    
    # Initialize Vertex AI for enterprise deployment [4]
    vertexai.init(project=project_id, location="us-central1")
    
    # Use Flash model (faster and often more reliable) [5]
    model = GenerativeModel("gemini-1.5-flash")
    
    print("✅ Gemini Flash initialized via Vertex AI")
    return model

def test_gemini_connection():
    """Test Gemini API connectivity"""
    try:
        model = initialize_gemini()
        
        # Simple test prompt with proper error handling
        response = model.generate_content(
            "Hello! Please respond with 'Gemini is working' to confirm the connection."
        )
        
        if response and response.text:
            print("✅ Gemini API test successful")
            print(f"Response: {response.text}")
            return True
        else:
            print("❌ Gemini API returned empty response")
            return False
            
    except Exception as e:
        print(f"❌ Gemini API test failed: {e}")
        # Let's see more details about the error
        print(f"Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    test_gemini_connection()