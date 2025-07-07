from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)
API_KEY = os.getenv("API_KEY")  # your API key must be set in .env
MODEL = "deepseek/deepseek-chat"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost",
    "X-Title": "DeepSeek Terminal Chatbot"
}

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        messages = data.get('messages', [])
        payload = {
            "model": MODEL,
            "messages": messages
        }

        response = requests.post(API_URL, headers=HEADERS, json=payload)
        return jsonify(response.json()), response.status_code

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
