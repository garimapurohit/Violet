from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import requests

# Load .env
load_dotenv()
app = Flask(__name__)
CORS(app, supports_credentials=True)

API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("MODEL", "deepseek/deepseek-chat")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost",  # required by OpenRouter
    "X-Title": "DeepSeek Chatbot"
}

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    messages = data.get("messages", [])

    payload = {
        "model": MODEL,
        "messages": messages
    }

    try:
        response = requests.post(API_URL, headers=HEADERS, json=payload)
        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"]
            return jsonify({"reply": reply})
        else:
            return jsonify({"error": "API call failed", "details": response.text}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
