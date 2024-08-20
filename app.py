from flask import Flask, render_template, request, jsonify, session
from src.config import load_config
from src.jira_utils import connect_to_jira
from src.rag import initialize_models, rag_jira

app = Flask(__name__)
app.secret_key = 'theconstellationisacollectionofmilkyways'  # Change this to a random secret key

config = load_config()
jira = connect_to_jira(config)
llm, embed_model = initialize_models(config)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    issue_id = request.form['issue_id']
    num_similar_issues = int(request.form.get('num_similar_issues', 2))
    
    results = rag_jira(issue_id, config, jira, llm, embed_model, num_similar_issues)
    
    # Store the search in session
    if 'searches' not in session:
        session['searches'] = []
    session['searches'].insert(0, {'issue_id': issue_id, 'results': results})
    session.modified = True
    
    return jsonify(results)

@app.route('/past_searches')
def past_searches():
    return jsonify(session.get('searches', []))

if __name__ == '__main__':
    app.run(debug=True)