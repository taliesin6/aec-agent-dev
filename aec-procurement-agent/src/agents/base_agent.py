# src/agents/base_agent.py - UPDATED FOR PHASE 3

import sys
import os
import json

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from google.adk.agents import Agent
from agents.pdf_tools import create_pdf_analysis_tool
from agents.material_intelligence_tools import create_material_intelligence_tool  # New import

def create_pdf_parser_agent():
    """Create PDF parser agent with multimodal analysis capabilities [1]"""
    pdf_analysis_tool = create_pdf_analysis_tool()
    
    pdf_parser = Agent(
        name="pdf_parser",
        description="Extracts material information from construction documents using GPT-4o vision",
        instruction="Analyze PDF construction documents using multimodal AI and extract structured material data with quantities, specifications, and categorization",
        tools=[pdf_analysis_tool]
    )
    
    return pdf_parser

def create_material_agent():
    """Create material intelligence agent with construction knowledge [1]"""
    material_intelligence_tool = create_material_intelligence_tool()
    
    material_agent = Agent(
        name="material_intelligence", 
        description="Standardizes and categorizes material data using construction industry knowledge",
        instruction="Apply construction intelligence to clean, standardize, and enhance extracted material information with Indonesian building standards and procurement data. Convert raw material lists into standardized construction specifications.",
        tools=[material_intelligence_tool]
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
    
    # Create coordinator with sub-agents [1]
    coordinator = Agent(
        name="procurement_coordinator",
        description="Coordinates multi-agent construction procurement workflow",
        instruction="Orchestrate PDF parsing, material analysis, and supplier matching for AEC procurement automation. Process documents through the complete pipeline from PDF extraction to supplier recommendations.",
        sub_agents=[pdf_agent, material_agent, supplier_agent]
    )
    
    return coordinator

def test_phase3_workflow():
    """Test the complete Phase 3 workflow: PDF → Material Intelligence"""
    print("🚀 Testing Phase 3: PDF Parser → Material Intelligence Workflow...")
    print("=" * 70)
    
    try:
        # Step 1: PDF Processing
        print("\n1️⃣ PDF Processing...")
        pdf_agent = create_pdf_parser_agent()
        
        # Check if sample PDF exists
        pdf_path = "sample_documents/house_floor_plan.pdf"
        if not os.path.exists(pdf_path):
            print(f"❌ PDF file not found: {pdf_path}")
            # Create mock PDF result for testing
            mock_pdf_result = {
                "project_name": "Test House Project", 
                "materials": [
                    {"name": "Concrete", "category": "structural", "quantity": 20, "unit": "m³", "drawing_reference": "Foundation"},
                    {"name": "Steel Rebar", "category": "structural", "quantity": 1500, "unit": "kg", "drawing_reference": "Foundation"},
                    {"name": "Bricks", "category": "structural", "quantity": 5000, "unit": "pcs", "drawing_reference": "Walls"},
                    {"name": "Tiles", "category": "finishes", "quantity": 200, "unit": "m²", "drawing_reference": "Flooring"},
                    {"name": "Paint", "category": "finishes", "quantity": 100, "unit": "liters", "drawing_reference": "Interior"},
                    {"name": "Electrical Wiring", "category": "mep", "quantity": 500, "unit": "m", "drawing_reference": "Electrical"},
                    {"name": "Plumbing Pipes", "category": "mep", "quantity": 100, "unit": "m", "drawing_reference": "Plumbing"},
                    {"name": "Doors", "category": "other", "quantity": 10, "unit": "pcs", "drawing_reference": "Openings"},
                    {"name": "Windows", "category": "other", "quantity": 15, "unit": "pcs", "drawing_reference": "Openings"}
                ],
                "confidence_score": 0.85,
                "processing_status": "success"
            }
            pdf_result = mock_pdf_result
            print("📝 Using mock PDF data for testing")
        else:
            with open(pdf_path, "rb") as f:
                pdf_content = f.read()
            # Get the tool function directly
            pdf_tool = pdf_agent.tools[0]
            pdf_result_json = pdf_tool(pdf_content, "house_floor_plan.pdf")
            pdf_result = json.loads(pdf_result_json) if isinstance(pdf_result_json, str) else pdf_result_json
        
        print(f"✅ PDF extracted {len(pdf_result.get('materials', []))} materials")
        
        # Step 2: Material Intelligence Processing  
        print("\n2️⃣ Material Intelligence Processing...")
        material_agent = create_material_agent()
        
        # Get the material intelligence tool function
        material_tool = material_agent.tools[0]
        enhanced_result_json = material_tool(json.dumps(pdf_result))
        enhanced_result = json.loads(enhanced_result_json) if isinstance(enhanced_result_json, str) else enhanced_result_json
        
        print(f"✅ Enhanced {len(enhanced_result.get('standardized_materials', []))} materials")
        
        # Step 3: Results Summary
        print("\n📊 Phase 3 Workflow Results:")
        print("=" * 50)
        print(f"Project Name: {enhanced_result.get('project_name', 'Unknown')}")
        print(f"Original materials: {len(pdf_result.get('materials', []))}")
        print(f"Enhanced materials: {len(enhanced_result.get('standardized_materials', []))}")
        
        metadata = enhanced_result.get('enhancement_metadata', {})
        print(f"Materials standardized: {metadata.get('materials_standardized', 0)}")
        print(f"Enhancement confidence: {metadata.get('enhancement_confidence', 0)}")
        print(f"Indonesian standards applied: {metadata.get('indonesian_standards_applied', False)}")
        
        # Step 4: Sample enhanced materials
        print("\n🔍 Sample Enhanced Materials:")
        standardized = enhanced_result.get('standardized_materials', [])
        for i, material in enumerate(standardized[:3]):  # Show first 3
            print(f"\n   {i+1}. {material.get('name', 'Unknown')} ({material.get('material_id', 'No ID')})")
            print(f"      Category: {material.get('category', 'Unknown')}")
            print(f"      Quantity: {material.get('quantity', 0)} {material.get('unit', 'units')}")
            print(f"      SNI Code: {material.get('indonesian_standards', {}).get('sni_code', 'N/A')}")
            print(f"      Confidence: {material.get('confidence_score', 0)}")
        
        if len(standardized) > 3:
            print(f"   ... and {len(standardized) - 3} more materials")
        
        print("\n✅ Phase 3 Workflow COMPLETED SUCCESSFULLY!")
        return enhanced_result
        
    except Exception as e:
        print(f"\n❌ Phase 3 workflow failed: {e}")
        import traceback
        print("Error details:", traceback.format_exc())
        return None

def test_adk_integration():
    """Test ADK multi-agent integration"""
    print("\n🔧 Testing ADK Multi-Agent Integration...")
    
    try:
        # Test individual agents
        pdf_agent = create_pdf_parser_agent()
        material_agent = create_material_agent()
        
        print(f"✅ PDF Parser Agent: {pdf_agent.name}")
        print(f"✅ Material Intelligence Agent: {material_agent.name}")
        print(f"✅ PDF Agent tools: {len(pdf_agent.tools)}")
        print(f"✅ Material Agent tools: {len(material_agent.tools)}")
        
        # Test multi-agent system
        coordinator = create_multi_agent_system()
        print(f"✅ Coordinator Agent: {coordinator.name}")
        print(f"✅ Sub-agents: {len(coordinator.sub_agents)}")
        
        print("✅ ADK Integration Test PASSED")
        return True
        
    except Exception as e:
        print(f"❌ ADK Integration Test FAILED: {e}")
        return False

if __name__ == "__main__":
    print("🚀 PHASE 3 COMPREHENSIVE TESTING")
    print("=" * 80)
    
    # Test 1: ADK Integration
    adk_success = test_adk_integration()
    
    # Test 2: End-to-End Workflow
    if adk_success:
        workflow_result = test_phase3_workflow()
        
        if workflow_result:
            print("\n🎯 PHASE 3 STATUS: ✅ READY FOR PHASE 4")
            print("📋 Next Phase: Supplier Matching Agent Development")
        else:
            print("\n⚠️  PHASE 3 STATUS: ❌ NEEDS DEBUGGING")
    else:
        print("\n⚠️  PHASE 3 STATUS: ❌ ADK INTEGRATION ISSUES")