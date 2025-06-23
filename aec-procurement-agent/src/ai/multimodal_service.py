# src/ai/multimodal_service.py
import os
from dotenv import load_dotenv

load_dotenv()

def get_multimodal_model():
    """Get available multimodal model with fallback strategy [1]"""
    
    # Try Gemini first (bonus points [1])
    try:
        if os.getenv("USE_OPENAI_BACKUP", "false").lower() != "true":
            import vertexai
            from vertexai.generative_models import GenerativeModel
            
            project_id = os.getenv("PROJECT_ID")
            vertexai.init(project=project_id, location="us-central1")
            model = GenerativeModel("gemini-1.5-flash")
            
            print("✅ Using Gemini Vision Pro for multimodal processing")
            return model, "gemini"
    except Exception as e:
        print(f"⚠️  Gemini unavailable: {e}")
        
    # Fallback to OpenAI (reliable backup [1])
    try:
        import openai  # Import here, inside the try block
        
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
            
        # Set up OpenAI client properly [2]
        openai.api_key = api_key
        print("✅ Using OpenAI GPT-4V as backup for multimodal processing")
        return openai, "openai"
    except Exception as e:
        print(f"❌ OpenAI setup failed: {e}")
        
    return None, None

def test_multimodal_service():
    """Test multimodal AI service with fallback"""
    print("Testing multimodal AI service...")
    
    model, service_type = get_multimodal_model()
    
    if service_type == "gemini":
        try:
            response = model.generate_content("Hello, this is a test message")
            print(f"✅ Gemini test successful: {response.text[:50]}...")
            return True
        except Exception as e:
            print(f"❌ Gemini test failed: {e}")
            return False
            
    elif service_type == "openai":
        try:
            # Updated for newer OpenAI API [4]
            import openai
            
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": "Hello, this is a test message"}],
                max_tokens=50
            )
            print(f"✅ OpenAI test successful: {response.choices[0].message.content}")
            return True
        except Exception as e:
            print(f"❌ OpenAI test failed: {e}")
            return False
    else:
        print("❌ No multimodal service available")
        return False

if __name__ == "__main__":
    test_multimodal_service()