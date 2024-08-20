from llama_index.llms import Ollama
from llama_index.embeddings import OllamaEmbedding
from llama_index import VectorStoreIndex, ServiceContext
from src.jira_utils import fetch_jira_issue, get_issue_summary, get_issue_comments, index_jira_data, get_similar_issues

def initialize_models(config):
    llm = Ollama(model=config["OLLAMA_MODEL"])
    embed_model = OllamaEmbedding(model_name=config["OLLAMA_MODEL"])
    return llm, embed_model

def rag_jira(issue_id, config, jira, llm, embed_model, num_similar_issues=2):
    # Fetch the issue
    issue = fetch_jira_issue(jira, issue_id)

    # Get issue details
    issue_summary = issue.fields.summary
    issue_description = issue.fields.description
    issue_created = issue.fields.created
    issue_priority = issue.fields.priority.name if issue.fields.priority else "No priority"
    issue_assignee = issue.fields.assignee.displayName if issue.fields.assignee else "Unassigned"

    # Summarize issue description
    description_summary = llm.complete(f"Summarize this JIRA issue description in one sentence:\n{issue_description}").text

    # Find similar issues
    documents = index_jira_data(jira, config)
    service_context = ServiceContext.from_defaults(llm=llm, embed_model=embed_model)
    index = VectorStoreIndex.from_documents(documents, service_context=service_context)
    similar_issues = get_similar_issues(index, issue_description, issue_id, embed_model, top_k=num_similar_issues)

    return {
        "issue_id": issue_id,
        "assignee": issue_assignee,
        "created": issue_created,
        "priority": issue_priority,
        "title": issue_summary,
        "description": issue_description,
        "description_summary": description_summary,      
        "similar_issues": similar_issues
    }