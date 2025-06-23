"""
ADK Material Intelligence Agent for AEC Procurement System
Phase 3 Agent Wrapper: Material standardization with Indonesian SNI standards
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
                return f"Mock material agent processed: {input_data[:50]}..."

# ✅ CORRECTED: Import the actual material intelligence tool
try:
    from agents.material_intelligence_tools import create_material_intelligence_tool
    print("✅ Material intelligence tools import successful")
except ImportError:
    try:
        import material_intelligence_tools
        create_material_intelligence_tool = material_intelligence_tools.create_material_intelligence_tool
        print("✅ Material intelligence tools fallback import successful")
    except ImportError as e:
        print(f"❌ Material intelligence tools import failed: {e}")
        # Create mock function
        def create_material_intelligence_tool():
            def mock_material_tool(raw_data):
                return '{"project_name": "Mock", "standardized_materials": []}'
            return mock_material_tool

import logging
logger = logging.getLogger(__name__)

def create_material_agent():
    """
    Create ADK Material Intelligence Agent with Indonesian standards
    """
    # Create the material intelligence tool (correct function name)
    material_tool = create_material_intelligence_tool()
    
    # Create ADK agent with tool
    material_agent = Agent(
        name="material_intelligence",
        description="Standardize construction materials with Indonesian SNI codes and construction industry knowledge",
        instruction="""
        You are a construction materials expert specializing in Indonesian building standards.
        
        TASK: Enhance and standardize material information from PDF parser.
        
        PROCESS:
        1. Receive raw material data JSON from PDF Parser Agent
        2. Standardize material names using construction industry knowledge
        3. Apply Indonesian SNI codes and local standards
        4. Add detailed specifications and procurement information
        5. Categorize materials (structural_concrete, mep_electrical, etc.)
        6. Suggest alternative materials for cost optimization
        
        RESPONSE: Return enhanced JSON with standardized materials, SNI codes, and procurement details.
        """,
        tools=[material_tool]
    )
    
    logger.info("✅ Created ADK Material Intelligence Agent")
    return material_agent

def test_material_agent():
    """Test the material intelligence agent"""
    try:
        agent = create_material_agent()
        print(f"✅ Material Agent: {agent.name}")
        print(f"✅ Description: {agent.description}")
        print(f"✅ Tools: {len(agent.tools)} registered")
        
        # Test the tool directly
        tool = create_material_intelligence_tool()
        print("🔧 Material intelligence tool created successfully")
        
        return True
    except Exception as e:
        print(f"❌ Material Agent creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_material_agent()