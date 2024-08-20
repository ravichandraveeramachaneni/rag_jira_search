from src.config import load_config

def test_config_loading():
    config = load_config()
    assert 'JIRA_SERVER' in config
    assert 'JIRA_EMAIL' in config
    assert 'JIRA_PROJECT' in config
    assert 'JIRA_API_TOKEN' in config
    assert 'OLLAMA_MODEL' in config
    assert config['JIRA_SERVER'] == ""  # Hardcoded atlassian URL for managing env config issues.