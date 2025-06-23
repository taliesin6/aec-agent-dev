# src/test_phase3_integration.py

import json
import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from agents.base_agent import (
    create_multi_agent_system,
    create_pdf_parser_agent, 
    create_material_agent,
    test_phase3_workflow,
    test_adk_integration
)
from agents.material_intelligence_tools import test_material_intelligence

def comprehensive_phase3_test():
    """Comprehensive Phase 3 testing suite"""
    print("🧪 PHASE 3 COMPREHENSIVE TESTING SUITE")
    print("=" * 80)
    
    test_results = {
        "material_intelligence_tool": False,
        "agent_integration": False,
        "workflow_end_to_end": False,
        "data_quality": False,
        "adk_compliance": False
    }
    
    # Test 1: Material Intelligence Tool (Standalone)
    print("\n1️⃣ Testing Material Intelligence Tool (Standalone)...")
    try:
        tool_result = test_material_intelligence()
        if tool_result and 'standardized_materials' in tool_result:
            materials_count = len(tool_result['standardized_materials'])
            confidence = tool_result.get('enhancement_metadata', {}).get('enhancement_confidence', 0)
            
            if materials_count > 0 and confidence > 0.5:
                test_results["material_intelligence_tool"] = True
                print(f"✅ Material Intelligence Tool: PASS ({materials_count} materials, {confidence} confidence)")
            else:
                print(f"❌ Material Intelligence Tool: FAIL (low quality: {materials_count} materials, {confidence} confidence)")
        else:
            print("❌ Material Intelligence Tool: FAIL (no valid output)")
    except Exception as e:
        print(f"❌ Material Intelligence Tool Error: {e}")
    
    # Test 2: ADK Agent Integration
    print("\n2️⃣ Testing ADK Agent Integration...")
    try:
        integration_success = test_adk_integration()
        if integration_success:
            test_results["agent_integration"] = True
            print("✅ ADK Agent Integration: PASS")
        else:
            print("❌ ADK Agent Integration: FAIL")
    except Exception as e:
        print(f"❌ ADK Agent Integration Error: {e}")
    
    # Test 3: Individual Agent Creation
    print("\n3️⃣ Testing Individual Agents...")
    try:
        material_agent = create_material_agent()
        
        # Check agent properties
        agent_checks = {
            "has_name": hasattr(material_agent, 'name') and material_agent.name == "material_intelligence",
            "has_description": hasattr(material_agent, 'description'),
            "has_tools": hasattr(material_agent, 'tools') and len(material_agent.tools) > 0,
            "tool_callable": callable(material_agent.tools[0]) if material_agent.tools else False
        }
        
        if all(agent_checks.values()):
            test_results["adk_compliance"] = True
            print("✅ ADK Compliance: PASS")
            for check, result in agent_checks.items():
                print(f"   {check}: {'✅' if result else '❌'}")
        else:
            print("❌ ADK Compliance: FAIL")
            for check, result in agent_checks.items():
                print(f"   {check}: {'✅' if result else '❌'}")
                
    except Exception as e:
        print(f"❌ ADK Compliance Error: {e}")
    
    # Test 4: End-to-End Workflow
    print("\n4️⃣ Testing End-to-End Workflow...")
    try:
        workflow_result = test_phase3_workflow()
        if workflow_result and 'standardized_materials' in workflow_result:
            test_results["workflow_end_to_end"] = True
            print("✅ End-to-End Workflow: PASS")
            
            # Test 5: Data Quality Assessment
            print("\n5️⃣ Testing Data Quality...")
            materials = workflow_result.get('standardized_materials', [])
            metadata = workflow_result.get('enhancement_metadata', {})
            
            quality_checks = {
                "materials_count": len(materials) > 0,
                "material_ids": all('material_id' in mat for mat in materials),
                "specifications": all('specifications' in mat for mat in materials),
                "indonesian_standards": all('indonesian_standards' in mat for mat in materials), 
                "procurement_info": all('procurement_info' in mat for mat in materials),
                "confidence_scores": all('confidence_score' in mat for mat in materials),
                "enhancement_confidence": metadata.get('enhancement_confidence', 0) > 0.5,
                "standardized_count": metadata.get('materials_standardized', 0) > 0
            }
            
            quality_score = sum(quality_checks.values()) / len(quality_checks)
            
            if quality_score >= 0.8:  # 80% pass rate
                test_results["data_quality"] = True
                print(f"✅ Data Quality: PASS ({quality_score:.1%} quality score)")
            else:
                print(f"❌ Data Quality: FAIL ({quality_score:.1%} quality score)")
                
            # Detailed quality breakdown
            print("   Quality Breakdown:")
            for check, result in quality_checks.items():
                print(f"     {check}: {'✅' if result else '❌'}")
                
        else:
            print("❌ End-to-End Workflow: FAIL")
    except Exception as e:
        print(f"❌ End-to-End Workflow Error: {e}")
    
    # Final Results Summary
    print("\n" + "=" * 80)
    print("🎯 PHASE 3 TEST SUMMARY")
    print("=" * 80)
    
    passed_tests = sum(test_results.values())
    total_tests = len(test_results)
    
    for test_name, result in test_results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:30} {status}")
    
    overall_score = passed_tests / total_tests
    print(f"\nOverall Result: {passed_tests}/{total_tests} tests passed ({overall_score:.1%})")
    
    if overall_score >= 0.8:  # 80% success rate
        print("🚀 PHASE 3 STATUS: READY FOR PHASE 4")
        print("📋 Next Phase: Supplier Matching Agent Development")
        return True
    else:
        print("⚠️  PHASE 3 STATUS: NEEDS FIXES")
        if overall_score >= 0.6:
            print("💡 Suggestion: Fix failing tests and proceed with caution")
        else:
            print("🔧 Suggestion: Major fixes required before Phase 4")
        return False

def quick_demo():
    """Quick demonstration of Phase 3 functionality"""
    print("\n🎬 QUICK PHASE 3 DEMO")
    print("=" * 50)
    
    # Demo material transformation
    print("📝 Demo: Material Transformation")
    
    sample_input = {
        "project_name": "Demo House",
        "materials": [
            {"name": "Concrete", "category": "structural", "quantity": 25, "unit": "m³"},
            {"name": "Steel Rebar", "category": "structural", "quantity": 2000, "unit": "kg"},
            {"name": "Paint", "category": "finishes", "quantity": 50, "unit": "liters"},
            {"name": "Mystery Material XYZ", "category": "other", "quantity": 100, "unit": "pieces"}
        ]
    }
    
    print(f"Input: {len(sample_input['materials'])} raw materials")
    
    # Process through material intelligence
    from agents.material_intelligence_tools import create_material_intelligence_tool
    tool = create_material_intelligence_tool()
    result = tool(json.dumps(sample_input))
    output = json.loads(result)
    
    print(f"Output: {len(output['standardized_materials'])} enhanced materials")
    print(f"Enhancement confidence: {output['enhancement_metadata']['enhancement_confidence']}")
    
    # Show transformation examples
    print("\n🔄 Transformation Examples:")
    for i, material in enumerate(output['standardized_materials'][:2]):
        original = sample_input['materials'][i]
        print(f"\n   {i+1}. {original['name']} → {material['name']}")
        print(f"      Category: {original.get('category', 'unknown')} → {material['category']}")
        print(f"      SNI Code: {material['indonesian_standards']['sni_code']}")
        print(f"      Confidence: {material['confidence_score']}")
    
    print("\n✅ Demo Complete!")

if __name__ == "__main__":
    # Run comprehensive test
    success = comprehensive_phase3_test()
    
    # Run quick demo
    quick_demo()
    
    # Final guidance
    if success:
        print("\n🎉 PHASE 3 COMPLETE - READY FOR PHASE 4!")
        print("📋 Next Steps:")
        print("   • Supplier Matching Agent Development")
        print("   • BigQuery Integration")
        print("   • Geographic Proximity Logic")
    else:
        print("\n🔧 PHASE 3 NEEDS ATTENTION")
        print("📋 Recommended Actions:")
        print("   • Fix failing tests")
        print("   • Check ADK agent integration")
        print("   • Verify material intelligence tool")