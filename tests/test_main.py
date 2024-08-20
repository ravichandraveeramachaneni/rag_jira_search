import pytest
from unittest.mock import patch
from src.main import main
from src.config import load_config
from src.rag import initialize_models
from llama_index import ServiceContext

@pytest.mark.parametrize("issue_id", [
    "R8-1",
    "R8-2",
])
def test_main_flow(issue_id):
    config = load_config()
    llm, embed_model = initialize_models(config)
    service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)
    
    mock_results = {
        "issue_id": issue_id,
        "title": "Test Title",
        "description": "Test Description",
        "description_summary": "Test Description Summary",
        "created": "2023-07-10",
        "priority": "High",
        "assignee": "John Doe",
        "similar_issues": [{"id": "R8-2", "summary": "Similar Issue", "created": "2023-07-09", "priority": "Medium", "assignee": "Jane Doe", "content": "Similar content"}]
    }
    
    with patch('src.main.load_config', return_value=config):
        with patch('src.main.connect_to_jira'):
            with patch('src.main.initialize_models', return_value=(llm, embed_model)):
                with patch('src.rag.rag_jira', return_value=mock_results):
                    with patch('builtins.input', side_effect=[issue_id, ""]):  # Simulate user input for issue_id and num_similar_issues
                        with patch('builtins.print') as mock_print:
                            main()
    
    # Check that something was printed (summaries and similar issues)
    assert mock_print.call_count > 0