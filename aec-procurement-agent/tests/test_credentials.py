# tests/test_credentials.py
import os
import sys
from dotenv import load_dotenv
from google.oauth2 import service_account
import json

# Add project root to path and load .env from root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(project_root)  # Change to project root
load_dotenv()  # Now .env will be found in project root

def test_credentials():
    project_id = os.getenv("PROJECT_ID")
    creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    print(f"Project ID: {project_id}")
    print(f"Credentials path: {creds_path}")
    print(f"Current directory: {os.getcwd()}")
    
    try:
        with open(creds_path, 'r') as f:
            creds_data = json.load(f)
            print(f"✅ Service account email: {creds_data.get('client_email')}")
    except Exception as e:
        print(f"❌ Credentials file error: {e}")

if __name__ == "__main__":
    test_credentials()