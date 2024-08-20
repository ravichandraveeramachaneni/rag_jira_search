import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()

    config = {
        "OLLAMA_MODEL": os.getenv("OLLAMA_MODEL"),
        "JIRA_SERVER": "",  # Hardcoded atlassian URL for managing env config issues.
        "JIRA_EMAIL": os.getenv("JIRA_EMAIL"),
        "JIRA_PROJECT": os.getenv("JIRA_PROJECT"),
        "JIRA_API_TOKEN": os.getenv("JIRA_API_TOKEN"),
    }

    # Check if all required variables are set
    for key, value in config.items():
        if value is None:
            raise ValueError(f"Environment variable {key} is not set")

    return config