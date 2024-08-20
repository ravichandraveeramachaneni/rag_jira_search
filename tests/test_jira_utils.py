from src.jira_utils import connect_to_jira, fetch_jira_issue, get_issue_summary, get_issue_comments, index_jira_data, get_similar_issues
from src.config import load_config
from llama_index import VectorStoreIndex, ServiceContext, Document
from src.rag import initialize_models
import pytest

def test_jira_connection():
    config = load_config()
    print("Loaded configuration:")
    for key, value in config.items():
        if key == 'JIRA_API_TOKEN':
            print(f"{key}: {'*' * len(value)}")
        else:
            print(f"{key}: {value}")
    
    jira = connect_to_jira(config)
    assert jira is not None, "JIRA connection failed"
    
    myself = jira.myself()
    assert myself['emailAddress'] == config['JIRA_EMAIL'], f"Email mismatch: {myself['emailAddress']} != {config['JIRA_EMAIL']}"
    print("JIRA connection test passed successfully")

def test_fetch_jira_issue():
    config = load_config()
    jira = connect_to_jira(config)
    # Replace "R8-1" with a valid issue ID from your JIRA project
    issue = fetch_jira_issue(jira, "R8-1")
    assert issue is not None
    assert issue.key == "R8-1"

def test_get_issue_summary():
    config = load_config()
    jira = connect_to_jira(config)
    # Replace "R8-1" with a valid issue ID from your JIRA project
    issue = fetch_jira_issue(jira, "R8-1")
    summary = get_issue_summary(issue)
    assert "Title:" in summary
    assert "Description:" in summary

def test_get_issue_comments():
    config = load_config()
    jira = connect_to_jira(config)
    # Replace "R8-1" with a valid issue ID from your JIRA project
    issue = fetch_jira_issue(jira, "R8-1")
    comments = get_issue_comments(issue)
    assert isinstance(comments, list)

def test_index_jira_data():
    config = load_config()
    jira = connect_to_jira(config)
    documents = index_jira_data(jira, config)
    assert len(documents) > 0
    assert all(isinstance(doc, Document) for doc in documents)

def test_get_similar_issues():
    config = load_config()
    jira = connect_to_jira(config)
    documents = index_jira_data(jira, config)
    llm, embed_model = initialize_models(config)
    service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)
    index = VectorStoreIndex.from_documents(documents, service_context=service_context)
    
    # Add a mock original_issue_id
    original_issue_id = "R8-1"
    
    similar_issues = get_similar_issues(index, "Test query", original_issue_id, embed_model)
    
    assert isinstance(similar_issues, list)
    assert len(similar_issues) <= 2  # Default is 2
    if similar_issues:
        assert "id" in similar_issues[0]
        assert "assignee" in similar_issues[0]
        assert "created" in similar_issues[0]
        assert "priority" in similar_issues[0]
        assert "title" in similar_issues[0]
        assert "content" in similar_issues[0]