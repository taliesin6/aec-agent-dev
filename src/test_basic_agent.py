# src/test_basic_agent.py
from google.adk.agents import Agent

def test_basic_agent():
    """Test basic ADK agent creation"""
    try:
        # Test minimal agent creation
        agent = Agent(name="test_agent")
        print(f"✅ Basic agent created: {agent}")
        
        # Test with description
        agent_with_desc = Agent(
            name="test_agent_2",
            description="Test agent description"
        )
        print(f"✅ Agent with description: {agent_with_desc}")
        
        return True
    except Exception as e:
        print(f"❌ Agent creation failed: {e}")
        return False

if __name__ == "__main__":
    test_basic_agent()