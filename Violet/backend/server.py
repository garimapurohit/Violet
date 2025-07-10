from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure CORS to allow requests from frontend
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://127.0.0.1:5500"],  
        "methods": ["POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# API Configuration
API_KEY = os.getenv("API_KEY")
MODEL = "deepseek/deepseek-chat"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Headers for API requests
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost",
    "X-Title": "DeepSeek Terminal Chatbot"
}

@app.route('/')
def home():
    """Simple health check endpoint"""
    return 'Flask backend is running!'

def _build_cors_preflight_response():
    """Helper function for CORS preflight requests"""
    response = jsonify({"success": True})
    response.headers.add("Access-Control-Allow-Origin", "http://127.0.0.1:5500")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type")
    return response

@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def chat():
    """Main chat endpoint"""
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()
    
    try:
        # Get and validate input
        data = request.get_json()
        if not data or 'messages' not in data:
            return jsonify({
                "success": False,
                "error": "Invalid request format"
            }), 400

        # Prepare payload for API
        payload = {
            "model": MODEL,
            "messages": data['messages']
        }

        # Call the AI API
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()  
        
        # Parse and standardize the response
        api_response = response.json()
        ai_message = api_response.get("choices", [{}])[0].get("message", {}).get("content", "No response")

        return jsonify({
            "success": True,
            "message": ai_message
        })

    except requests.exceptions.RequestException as e:
        return jsonify({
            "success": False,
            "error": f"API request failed: {str(e)}"
        }), 500
    except Exception as e:
        return jsonify({
            "success": False,
            "error": f"Server error: {str(e)}"
        }), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)