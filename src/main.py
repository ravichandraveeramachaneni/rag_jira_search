from src.config import load_config
from src.jira_utils import connect_to_jira
from src.rag import initialize_models, rag_jira

def main():
    config = load_config()
    jira = connect_to_jira(config)
    llm, embed_model = initialize_models(config)

    issue_id = input("Enter JIRA issue ID: ")
    num_similar_issues = input("Enter number of similar issues to retrieve (default is 2): ")
    num_similar_issues = int(num_similar_issues) if num_similar_issues.isdigit() else 2

    results = rag_jira(issue_id, config, jira, llm, embed_model, num_similar_issues)

    print("\n--- Issue Details ---")
    print(f"Issue ID: {results['issue_id']}")
    print(f"Title: {results['title']}")
    print(f"Created: {results['created']}")
    print(f"Priority: {results['priority']}")
    print(f"Assignee: {results['assignee']}")
    print(f"\nDescription: {results['description'][:200]}...")  # Print first 200 characters
    print(f"\nDescription Summary: {results['description_summary']}")

    print("\n--- Similar Issues ---")
    for issue in results['similar_issues']:
        print(f"ID: {issue['id']}")
        print(f"URL: {config['JIRA_SERVER']}/browse/{issue['id']}")
        print(f"Summary: {issue['summary']}")
        print(f"Created: {issue['created']}")
        print(f"Priority: {issue['priority']}")
        print(f"Assignee: {issue['assignee']}")
        print(f"Content: {issue['content'][:100]}...")  # Print first 100 characters
        print()

if __name__ == "__main__":
    main()