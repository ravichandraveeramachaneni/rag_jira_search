import pytest
from src.rag import initialize_models, rag_jira
from src.config import load_config
from src.jira_utils import connect_to_jira
from unittest.mock import patch, MagicMock

def test_rag_functionality():
    config = load_config()
    jira = connect_to_jira(config)
    llm, embed_model = initialize_models(config)
    
    # Replace with a real JIRA issue ID from your system
    test_issue_id = "R8-1"
    
    # Create a mock issue
    mock_issue = MagicMock()
    mock_issue.fields.summary = "Test Issue Summary"
    mock_issue.fields.description = "Test Issue Description"
    
    with patch('src.jira_utils.fetch_jira_issue', return_value=mock_issue):
        with patch('src.rag.VectorStoreIndex.from_documents', return_value=None):
            with patch('src.rag.get_similar_issues', return_value=[{"id": "R8-2", "content": "Similar Issue"}]):
                results = rag_jira(test_issue_id, config, jira, llm, embed_model)
    
    assert 'issue_id' in results
    assert results['issue_id'] == test_issue_id
    assert 'title' in results
    assert 'description' in results
    assert 'description_summary' in results
    assert len(results['description_summary']) > 0
    assert 'similar_issues' in results
    assert isinstance(results['similar_issues'], list)
    assert len(results['similar_issues']) > 0