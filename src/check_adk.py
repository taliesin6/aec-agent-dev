# src/check_adk.py
from google.adk.agents import Agent
import inspect

def check_adk_agent_parameters():
    """Check what parameters ADK Agent accepts"""
    signature = inspect.signature(Agent.__init__)
    print("ADK Agent constructor parameters:")
    for param_name, param in signature.parameters.items():
        if param_name != 'self':
            print(f"  - {param_name}: {param}")

if __name__ == "__main__":
    check_adk_agent_parameters()
