"""
ADK PDF Parser Agent for AEC Procurement System
Phase 2 Agent Wrapper: PDF processing with GPT-4o Vision
"""

import sys
import os

# Add the parent directory to sys.path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

# ✅ ADK import
try:
    from google.adk import Agent
except ImportError:
    try: 
        from adk import Agent
    except ImportError:
        class Agent:
            def __init__(self, **kwargs):
                self.__dict__.update(kwargs)
            def process(self, input_data):
                return f"Mock PDF agent processed: {input_data[:50]}..."

# ✅ CORRECTED: Import the actual PDF processing tool
try:
    from agents.pdf_tools import create_pdf_analysis_tool
    print("✅ PDF tools import successful")
except ImportError:
    try:
        import pdf_tools
        create_pdf_analysis_tool = pdf_tools.create_pdf_analysis_tool
        print("✅ PDF tools fallback import successful") 
    except ImportError as e:
        print(f"❌ PDF tools import failed: {e}")
        # Create mock function
        def create_pdf_analysis_tool():
            def mock_pdf_tool(pdf_content, filename="mock.pdf"):
                return {
                    "project_name": "Mock Project",
                    "materials": [{"name": "Mock Material", "category": "structural", "quantity": 1, "unit": "unit"}],
                    "confidence_score": 0.8
                }
            return mock_pdf_tool

import logging
logger = logging.getLogger(__name__)

def create_pdf_parser_agent():
    """
    Create ADK PDF Parser Agent with GPT-4o Vision tool
    """
    # Create the PDF analysis tool (correct function name)
    pdf_tool = create_pdf_analysis_tool()
    
    # Create ADK agent with tool
    pdf_agent = Agent(
        name="pdf_parser",
        description="Extract materials and quantities from construction PDF documents using GPT-4o Vision",
        instruction="""
        You are a specialist in analyzing construction documents and extracting material information.
        
        TASK: Process PDF construction documents to extract materials and quantities.
        
        PROCESS:
        1. Receive PDF document bytes from user
        2. Use GPT-4o Vision to analyze drawings and specifications
        3. Extract material names, quantities, units, and specifications
        4. Identify drawing references and project information
        5. Return structured JSON with extracted materials
        
        RESPONSE: Return JSON with project name, materials list, and confidence scores.
        """,
        tools=[pdf_tool]
    )
    
    logger.info("✅ Created ADK PDF Parser Agent")
    return pdf_agent

def test_pdf_agent():
    """Test the PDF parser agent"""
    try:
        agent = create_pdf_parser_agent()
        print(f"✅ PDF Agent: {agent.name}")
        print(f"✅ Description: {agent.description}")
        print(f"✅ Tools: {len(agent.tools)} registered")
        
        # Test the tool directly
        tool = create_pdf_analysis_tool()
        print("🔧 PDF analysis tool created successfully")
        
        return True
    except Exception as e:
        print(f"❌ PDF Agent creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_pdf_agent()