from jira import JIRA
from bs4 import BeautifulSoup
import requests
from llama_index import VectorStoreIndex, Document
import numpy as np

def connect_to_jira(config):
    options = {
        'server': config['JIRA_SERVER'],
        'verify': True,
    }
    print(f"Connecting to JIRA server: {config['JIRA_SERVER']}")
    print(f"Using email: {config['JIRA_EMAIL']}")
    print(f"API Token length: {len(config['JIRA_API_TOKEN'])}")
    
    try:
        jira = JIRA(options, basic_auth=(config['JIRA_EMAIL'], config['JIRA_API_TOKEN']))
        myself = jira.myself()
        print(f"Successfully connected to JIRA as {myself['displayName']}")
        return jira
    except Exception as e:
        print(f"Failed to connect to JIRA. Error: {str(e)}")
        raise

def fetch_jira_issue(jira, issue_id):
    issue = jira.issue(issue_id)
    return issue

def get_issue_summary(issue):
    return f"Title: {issue.fields.summary}\nDescription: {issue.fields.description}"

def get_issue_comments(issue):
    comments = issue.fields.comment.comments
    return [comment.body for comment in comments]

def index_jira_data(jira, config):
    issues = jira.search_issues(f'project={config["JIRA_PROJECT"]}', maxResults=1000)
    documents = []
    for issue in issues:
        doc_content = (
            f"Key: {issue.key}\n"
            f"Summary: {issue.fields.summary}\n"
            f"Description: {issue.fields.description}\n"
            f"Created: {issue.fields.created}\n"
        )
        metadata = {
            "id": issue.key,
            "summary": issue.fields.summary,
            "created": str(issue.fields.created),
            "priority": str(issue.fields.priority) if issue.fields.priority else "No priority",
            "assignee": issue.fields.assignee.displayName if issue.fields.assignee else "Unassigned"
        }
        documents.append(Document(text=doc_content, metadata=metadata))
    return documents

def get_similar_issues(index, query, original_issue_id, embed_model, top_k=2):
    query_engine = index.as_query_engine()
    results = query_engine.query(query)
    similar_issues = []
    for node in results.source_nodes[:top_k+1]:  # Get one extra to filter out original issue
        issue_data = node.metadata
        if issue_data.get("id") != original_issue_id:
            similar_issues.append({
                "id": issue_data.get("id", "Unknown"),
                "assignee": issue_data.get("assignee", "Unassigned"),
                "created": issue_data.get("created", "Unknown"),
                "priority": issue_data.get("priority", "No priority"),
                "title": issue_data.get("summary", "No title"),
                "content": node.text
            })
        if len(similar_issues) == top_k:
            break
    return similar_issues