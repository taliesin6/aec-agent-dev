# src/agents/pdf_tools.py - UPDATED WITH PDF TO IMAGE CONVERSION
import base64
import json
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
import openai
from datetime import datetime
import os
from dotenv import load_dotenv
import fitz  # PyMuPDF for PDF processing
from PIL import Image
import io

# Load environment variables from .env file
load_dotenv()

@dataclass
class Material:
    name: str
    category: str  # "structural", "finishes", "mep", etc.
    quantity: float
    unit: str  # "m3", "kg", "pcs", etc.
    specifications: Optional[str] = None
    drawing_reference: Optional[str] = None

@dataclass
class ExtractedMaterials:
    project_name: str
    materials: List[Material]
    confidence_score: float
    extraction_timestamp: str

def pdf_to_images(pdf_content: bytes) -> List[str]:
    """Convert PDF pages to base64 encoded images"""
    try:
        # Open PDF from bytes
        pdf_document = fitz.open(stream=pdf_content, filetype="pdf")
        images = []
        
        # Convert each page to image
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            
            # Render page as image (300 DPI for good quality)
            mat = fitz.Matrix(2.0, 2.0)  # 2x zoom = ~300 DPI
            pix = page.get_pixmap(matrix=mat)
            
            # Convert to PIL Image
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data))
            
            # Convert to base64
            buffer = io.BytesIO()
            img.save(buffer, format='PNG')
            img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            images.append(img_base64)
        
        pdf_document.close()
        print(f"📄 Converted PDF to {len(images)} images")
        return images
        
    except Exception as e:
        print(f"❌ PDF conversion failed: {e}")
        return []

def create_pdf_analysis_tool():
    """Create PDF processing tool for ADK agent integration"""
    
    def analyze_construction_pdf(pdf_content: bytes, filename: str = "construction_doc.pdf") -> dict:
        """
        Analyze construction PDF using GPT-4V multimodal capabilities
        Returns structured material data for ADK agent processing
        """
        try:
            print(f"🔍 Analyzing PDF: {filename}")
            print(f"📊 Content size: {len(pdf_content)} bytes")
            
            # Verify API key is available
            api_key = os.getenv('OPENAI_API_KEY')
            if not api_key:
                raise ValueError("OpenAI API key not found in environment variables")
            
            print(f"🔑 API Key loaded: {'Yes' if api_key else 'No'}")
            
            # Convert PDF to images first
            print("🔄 Converting PDF to images...")
            images = pdf_to_images(pdf_content)
            
            if not images:
                raise ValueError("Failed to convert PDF to images")
            
            # Use only the first page for now (can expand later)
            first_page_image = images[0]
            
            # Construction-specific prompt optimized for Indonesian documents
            extraction_prompt = """
            Analyze this construction document (floor plan, BoQ, or specification) and extract material information.
            
            Look for construction materials such as:
            - Structural: concrete, steel rebar, bricks, blocks, foundation materials
            - Finishes: tiles, paint, flooring, ceiling, wall finishes
            - MEP: electrical, plumbing, HVAC components
            - Others: doors, windows, fixtures, hardware
            
            Extract and structure the data as JSON:
            {
                "project_name": "extracted project name or 'House Project'",
                "materials": [
                    {
                        "name": "specific material name",
                        "category": "structural/finishes/mep/other", 
                        "quantity": numerical_value,
                        "unit": "m³/m²/kg/pcs/etc",
                        "specifications": "detailed specs or null",
                        "drawing_reference": "room/section reference or null"
                    }
                ],
                "confidence_score": 0.85
            }
            
            Be precise with material names and quantities. For Indonesian documents, translate material names to English.
            If this is a floor plan, estimate typical materials needed for the visible rooms and structure.
            """
            
            # Initialize OpenAI client with explicit API key
            client = openai.OpenAI(api_key=api_key)
            
            print("🤖 Sending to GPT-4o for analysis...")
            
            response = client.chat.completions.create(
                model="gpt-4o",  # Current model with vision
                messages=[
                    {
                        "role": "user", 
                        "content": [
                            {"type": "text", "text": extraction_prompt},
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/png;base64,{first_page_image}",
                                    "detail": "high"
                                }
                            }
                        ]
                    }
                ],
                max_tokens=2500,
                temperature=0.1
            )
            
            result_text = response.choices[0].message.content
            print("✅ GPT-4o Response received")
            
            # Extract JSON from response
            try:
                start_idx = result_text.find('{')
                end_idx = result_text.rfind('}') + 1
                
                if start_idx != -1 and end_idx > start_idx:
                    json_str = result_text[start_idx:end_idx]
                    result_data = json.loads(json_str)
                    
                    # Add timestamp and metadata
                    result_data['extraction_timestamp'] = datetime.now().isoformat()
                    result_data['source_filename'] = filename
                    result_data['processing_status'] = 'success'
                    result_data['pages_processed'] = len(images)
                    
                    print(f"📋 Extracted {len(result_data.get('materials', []))} materials")
                    return result_data
                else:
                    raise json.JSONDecodeError("No JSON found", result_text, 0)
                    
            except json.JSONDecodeError as e:
                print(f"⚠️ JSON parsing failed: {e}")
                # Create fallback response with raw text for debugging
                return {
                    "project_name": filename.replace('.pdf', ''),
                    "materials": [],
                    "confidence_score": 0.3,
                    "extraction_timestamp": datetime.now().isoformat(),
                    "processing_status": "json_parse_failed",
                    "raw_response": result_text[:1000],  # First 1000 chars for debugging
                    "error": f"JSON parsing failed: {str(e)}"
                }
                
        except Exception as e:
            print(f"❌ PDF analysis failed: {e}")
            return {
                "project_name": filename.replace('.pdf', '') if filename else "Unknown",
                "materials": [],
                "confidence_score": 0.0,
                "extraction_timestamp": datetime.now().isoformat(),
                "processing_status": "extraction_failed", 
                "error": str(e)
            }
    
    return analyze_construction_pdf

# Test function for standalone testing
def test_pdf_tool():
    """Test the PDF analysis tool independently"""
    print("🧪 Testing PDF Analysis Tool...")
    
    # Debug: Check environment variables
    print("🔍 Environment Check:")
    print(f"OPENAI_API_KEY set: {'Yes' if os.getenv('OPENAI_API_KEY') else 'No'}")
    
    tool = create_pdf_analysis_tool()
    
    # Test with a sample file
    try:
        with open("sample_documents/house_floor_plan.pdf", "rb") as f:
            pdf_content = f.read()
            
        result = tool(pdf_content, "house_floor_plan.pdf")
        
        print("🎯 Test Results:")
        print(json.dumps(result, indent=2))
        
        return result
        
    except FileNotFoundError:
        print("📁 Sample document not found. Please add your Indonesian floor plan to sample_documents/")
        return None

if __name__ == "__main__":
    test_pdf_tool()