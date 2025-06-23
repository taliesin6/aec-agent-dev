# src/test_phase2_integration.py
import json
from agents.base_agent import (
    create_multi_agent_system, 
    create_pdf_parser_agent, 
    test_multi_agent_pdf_workflow
)

def test_phase2_integration():
    """Comprehensive Phase 2 integration test"""
    print("🧪 Phase 2 Integration Testing")
    print("=" * 50)
    
    # Test 1: ADK Agent Creation
    print("\n1️⃣ Testing ADK Agent Creation...")
    try:
        coordinator = create_multi_agent_system()
        print(f"✅ Coordinator agent: {coordinator.name}")
        print(f"✅ Sub-agents: {len(coordinator.sub_agents)} agents")
        
        pdf_agent = create_pdf_parser_agent()
        print(f"✅ PDF agent: {pdf_agent.name}")
        print(f"✅ PDF agent tools: {len(pdf_agent.tools)} tools")
        
    except Exception as e:
        print(f"❌ Agent creation failed: {e}")
        return False
    
    # Test 2: Tool Integration
    print("\n2️⃣ Testing Tool Integration...")
    try:
        result = test_multi_agent_pdf_workflow()
        if result and result.get('processing_status') == 'success':
            print("✅ Tool integration working")
        else:
            print("❌ Tool integration failed")
            return False
    except Exception as e:
        print(f"❌ Tool integration error: {e}")
        return False
    
    # Test 3: Data Flow Validation
    print("\n3️⃣ Testing Data Flow...")
    try:
        materials = result.get('materials', [])
        if len(materials) > 0:
            print(f"✅ Material extraction: {len(materials)} materials")
            
            # Validate data structure
            sample_material = materials[0]
            required_fields = ['name', 'category', 'quantity', 'unit']
            
            for field in required_fields:
                if field in sample_material:
                    print(f"✅ Data field '{field}': {sample_material[field]}")
                else:
                    print(f"❌ Missing field: {field}")
                    return False
        else:
            print("❌ No materials extracted")
            return False
            
    except Exception as e:
        print(f"❌ Data flow validation failed: {e}")
        return False
    
    print("\n🎯 Phase 2 Integration: SUCCESS ✅")
    print("=" * 50)
    print(f"📋 Total materials extracted: {len(materials)}")
    print(f"📈 Confidence score: {result.get('confidence_score')}")
    print(f"⏱️ Processing time: {result.get('extraction_timestamp')}")
    
    return True

if __name__ == "__main__":
    success = test_phase2_integration()
    if success:
        print("\n🚀 Ready for Phase 3: Material Intelligence Agent")
    else:
        print("\n⚠️ Phase 2 issues need resolution")