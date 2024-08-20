import os
import requests
from dotenv import load_dotenv

def test_jira_connection():
    print("Contents of .env file:")
    with open('../.env', 'r') as env_file:
        print(env_file.read())

    print("\nLoading environment variables...")
    load_dotenv()

    jira_server = os.getenv('JIRA_SERVER')
    jira_email = os.getenv('JIRA_EMAIL')
    jira_api_token = os.getenv('JIRA_API_TOKEN')

    print(f"\nJIRA_SERVER from env: {jira_server}")
    print(f"JIRA_EMAIL from env: {jira_email}")
    print(f"API Token length: {len(jira_api_token) if jira_api_token else 'No token found'}")

    # Rest of the function remains the same...

if __name__ == "__main__":
    test_jira_connection()