from flask import Flask, request, jsonify
from src.honeypot_agent import HoneyPotAgent
import os
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration
API_KEY = os.environ.get("HONEYPOT_API_KEY", "hackathon-2026-secret")
conversations = {}

def get_or_create_agent(conversation_id):
    """Retrieves an existing agent for the ID or creates a new one."""
    if conversation_id not in conversations:
        conversations[conversation_id] = HoneyPotAgent(persona="naive_elderly")
    return conversations[conversation_id]

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

@app.route('/chat', methods=['POST'])
def chat_endpoint():
    try:
        # 1. Authentication
        auth_header = (
            request.headers.get('Authorization')
            or request.headers.get('x-api-key')
        )
        
        if not auth_header:
            logger.warning("Missing authentication header")
            return jsonify({"error": "Unauthorized"}), 401
        
        provided_key = auth_header.replace("Bearer ", "").strip()
        
        if provided_key != API_KEY:
            logger.warning(f"Invalid API key provided: {provided_key[:10]}...")
            return jsonify({"error": "Unauthorized"}), 401
        
        # 2. Extract Data
        data = request.json or {}
        logger.info(f"Received data: {data}")
        
        if not isinstance(data, dict):
            data = {}
        
        conversation_id = data.get("sessionId", "default-session")
        msg = data.get("message", {})
        
        if isinstance(msg, dict):
            message = msg.get("text", "Hello")
        else:
            message = str(msg) if msg else "Hello"
        
        logger.info(f"Processing message: {message[:50]}...")
        
        # 3. Process with Agent (with timeout protection)
        agent = get_or_create_agent(conversation_id)
        
        # Quick response generation
        response_text = agent.generate_response(message)
        
        # Background analysis (lightweight)
        try:
            agent.detect_scam(message)
            agent.extract_intelligence(message)
        except Exception as e:
            logger.error(f"Background analysis error: {e}")
            # Don't fail the response if analysis fails
        
        # 4. Construct Response (matching expected format exactly)
        response = {
            "status": "success",
            "reply": response_text
        }
        
        logger.info(f"Sending response: {response}")
        return jsonify(response), 200
        
    except Exception as e:
        logger.error(f"Error in chat_endpoint: {str(e)}")
        return jsonify({
            "status": "error",
            "reply": "I'm having trouble understanding. Could you say that again?"
        }), 500

@app.route('/', methods=['GET'])
def root():
    return jsonify({
        "service": "Honey-Pot API",
        "status": "running",
        "endpoints": ["/health", "/chat"]
    }), 200

# Error handlers
@app.errorhandler(404)
def not_found(e):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(e):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting Honey-Pot API on port {port}")
    logger.info(f"API Key configured: {API_KEY[:10]}...")
    app.run(host='0.0.0.0', port=port, debug=False)
