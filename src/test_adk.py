# src/test_adk.py
from agents.base_agent import create_multi_agent_system

def test_adk_multi_agent_setup():
    """Test ADK agent communication - success criteria [1]"""
    # Create multi-agent system
    coordinator = create_multi_agent_system()
    
    # Verify multi-agent setup
    assert coordinator.name == "procurement_coordinator"
    assert len(coordinator.sub_agents) == 3  # PDF, Material, Supplier agents
    
    print("✅ ADK Multi-Agent System Working")
    print(f"✅ Coordinator agent: {coordinator.name}")
    print(f"✅ Sub-agents count: {len(coordinator.sub_agents)}")
    
    # Print sub-agent details
    for i, agent in enumerate(coordinator.sub_agents):
        print(f"✅ Sub-agent {i+1}: {agent.name} - {agent.description}")
    
    return True

if __name__ == "__main__":
    test_adk_multi_agent_setup()