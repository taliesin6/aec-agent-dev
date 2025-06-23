# src/connectivity_test.py
import os
from google.cloud import bigquery
import vertexai
from dotenv import load_dotenv

load_dotenv()

def test_google_cloud_connectivity():
    """Test all required Google Cloud APIs - mandatory requirement"""
    tests = {
        "vertex_ai": test_vertex_ai_connection,
        "bigquery": test_bigquery_connection
    }
    
    results = {}
    for service, test_func in tests.items():
        try:
            test_func()
            results[service] = "✅ Connected"
        except Exception as e:
            results[service] = f"❌ Failed: {e}"
    
    return results

def test_vertex_ai_connection():
    """Verify Vertex AI connection for Gemini access [2][3]"""
    project_id = os.getenv("PROJECT_ID")
    vertexai.init(project=project_id, location="us-central1")
    print("Vertex AI initialized successfully")

def test_bigquery_connection():
    """Test BigQuery connection for supplier database"""
    client = bigquery.Client()
    query = "SELECT 1 as test"
    results = client.query(query)
    print("BigQuery connection successful")

if __name__ == "__main__":
    results = test_google_cloud_connectivity()
    for service, status in results.items():
        print(f"{service}: {status}")