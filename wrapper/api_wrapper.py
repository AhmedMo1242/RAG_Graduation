from flask import Flask, request, jsonify
from rag_manager.manager import RAGManager

app = Flask(__name__)
manager = RAGManager()

@app.route('/add_domain', methods=['POST'])
def add_domain():
    data = request.json
    domain_name = data.get('domain_name')
    model_name = data.get('model_name')
    if not domain_name or not model_name:
        return jsonify({"error": "Domain name and model name are required"}), 400
    manager.add_domain(domain_name, model_name)
    return jsonify({"message": f"Domain {domain_name} with model {model_name} added."}), 200

@app.route('/list_domains', methods=['GET'])
def list_domains():
    domains = manager.list_domains()
    return jsonify(domains), 200

@app.route('/add_data', methods=['POST'])
def add_data():
    data = request.json
    domain_name = data.get('domain_name')
    model_name = data.get('model_name')
    document = data.get('document')
    if not domain_name or not model_name or not document:
        return jsonify({"error": "Domain name, model name, and document are required"}), 400
    manager.add_data(domain_name, model_name, {"data": document})
    return jsonify({"message": f"Data added to domain {domain_name} with model {model_name}."}), 200

@app.route('/generate_prompt', methods=['POST'])
def generate_prompt():
    data = request.json
    domain_name = data.get('domain_name')
    model_name = data.get('model_name')
    query = data.get('query')
    mode = data.get('mode', 'hybrid')
    if not domain_name or not model_name or not query:
        return jsonify({"error": "Domain name, model name, and query are required"}), 400
    prompt = manager.generate_prompt(domain_name, model_name, query, mode)
    return jsonify({"prompt": prompt}), 200


