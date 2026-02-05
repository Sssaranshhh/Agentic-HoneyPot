from flask import Flask, request, jsonify
from src.honeypot_agent import HoneyPotAgent
import os

app = Flask(__name__)

# Configuration
API_KEY = os.environ.get("HONEYPOT_API_KEY", "secret-demo-key")
conversations = {}

def get_or_create_agent(conversation_id):
    """Retrieves an existing agent for the ID or creates a new one."""
    if conversation_id not in conversations:
        # We can randomize persona here if we want variety across conversations
        conversations[conversation_id] = HoneyPotAgent(persona="naive_elderly")
    return conversations[conversation_id]

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    # 1. Authentication
    auth_header = (
        request.headers.get('Authorization')
        or request.headers.get('x-api-key')
    )

    if not auth_header:
        return jsonify({"error": "Unauthorized"}), 401

    provided_key = auth_header.replace("Bearer ", "")
    
    if provided_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 401

    # 2. Extract Data
    data = request.json
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    conversation_id = data.get('conversation_id')
    message = data.get('message')

    if not conversation_id or not message:
        return jsonify({"error": "Missing conversation_id or message"}), 400

    # 3. Process with Agent
    agent = get_or_create_agent(conversation_id)
    
    # Run Agent Logic
    is_scam = agent.detect_scam(message)
    response_text = agent.generate_response(message)
    agent.extract_intelligence(message)

    # 4. Construct Response
    return jsonify({
        "conversation_id": conversation_id,
        "response": response_text,
        "scam_detected": is_scam,
        "extracted_intelligence": agent.extracted_data
    })

if __name__ == '__main__':
    print(f"Starting Honey-Pot API on port 5000...")
    print(f"Use API Key: {API_KEY}")
    app.run(host='0.0.0.0', port=5000)
