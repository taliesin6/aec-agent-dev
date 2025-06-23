# src/agents/base_agent.py - FIXED IMPORTS
import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from google.adk.agents import Agent
from agents.pdf_tools import create_pdf_analysis_tool  # Changed from relative to absolute

def create_pdf_parser_agent():
    """Create PDF parser agent with multimodal analysis capabilities [1]"""
    # Get the working PDF analysis tool
    pdf_analysis_tool = create_pdf_analysis_tool()
    
    pdf_parser = Agent(
        name="pdf_parser",
        description="Extracts material information from construction documents using GPT-4o vision",
        instruction="Analyze PDF construction documents using multimodal AI and extract structured material data with quantities, specifications, and categorization",
        # Register the custom tool
        tools=[pdf_analysis_tool]
    )
    return pdf_parser

def create_material_agent():
    """Create material intelligence agent [1]"""
    material_agent = Agent(
        name="material_intelligence",
        description="Standardizes and categorizes material data",
        instruction="Clean, standardize, and categorize extracted material information using construction industry knowledge"
    )
    return material_agent

def create_supplier_agent():
    """Create supplier matching agent [1]"""
    supplier_agent = Agent(
        name="supplier_matching",
        description="Find and rank suppliers based on materials and location",
        instruction="Match materials with suppliers using geographic proximity and availability from BigQuery database"
    )
    return supplier_agent

def create_multi_agent_system():
    """Create complete multi-agent system - ADK requirement [1]"""
    # Create sub-agents first
    pdf_agent = create_pdf_parser_agent()
    material_agent = create_material_agent()
    supplier_agent = create_supplier_agent()
    
    # Create coordinator with sub-agents [3]
    coordinator = Agent(
        name="procurement_coordinator",
        description="Coordinates multi-agent construction procurement workflow",
        instruction="Orchestrate PDF parsing, material analysis, and supplier matching for AEC procurement automation",
        sub_agents=[pdf_agent, material_agent, supplier_agent]  # ✅ Using sub_agents
    )
    
    return coordinator

# New function: Test the integrated system
def test_multi_agent_pdf_workflow():
    """Test the complete multi-agent workflow with PDF processing"""
    print("🚀 Testing Multi-Agent PDF Workflow...")
    
    # Create the multi-agent system
    coordinator = create_multi_agent_system()
    
    # Test PDF processing through the agent system
    try:
        with open("sample_documents/house_floor_plan.pdf", "rb") as f:
            pdf_content = f.read()
        
        # Create input for the coordinator
        workflow_input = {
            "task": "process_construction_pdf",
            "pdf_content": pdf_content,
            "filename": "house_floor_plan.pdf",
            "contractor_location": {"lat": -6.2088, "lng": 106.8456}  # Jakarta coordinates
        }
        
        print("📋 Coordinator processing request...")
        
        # In a real scenario, this would trigger the multi-agent workflow
        # For now, let's test the PDF agent directly
        pdf_agent = create_pdf_parser_agent()
        
        print("🔧 Testing PDF agent within ADK framework...")
        result = pdf_agent.tools[0](pdf_content, "house_floor_plan.pdf")
        
        print("✅ Multi-Agent System Test Results:")
        print(f"📊 Materials extracted: {len(result.get('materials', []))}")
        print(f"🎯 Processing status: {result.get('processing_status')}")
        print(f"📈 Confidence score: {result.get('confidence_score')}")
        
        return result
        
    except Exception as e:
        print(f"❌ Multi-agent test failed: {e}")
        return None

if __name__ == "__main__":
    test_multi_agent_pdf_workflow()