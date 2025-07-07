print("Details:", response.text)

import requests
import json

API_KEY = "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"  # Replace with your OpenRouter API key
MODEL = "deepseek/deepseek-chat"  # You can change to deepseek-coder or others
API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "HTTP-Referer": "http://localhost",  # required by OpenRouter policy
    "X-Title": "DeepSeek Terminal Chatbot"
}
def chat():
    print("🤖 DeepSeek Chatbot (type 'exit' to quit)\n")
    messages = []

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Assistant: Goodbye! 👋")
            break

        messages.append({"role": "user", "content": user_input})

        payload = {
            "model": MODEL,
            "messages": messages
        }

        try:
            response = requests.post(API_URL, headers=HEADERS, data=json.dumps(payload))
            if response.status_code == 200:
                reply = response.json()["choices"][0]["message"]["content"].strip()
                print("Assistant:", reply)
                messages.append({"role": "assistant", "content": reply})
            else:
                print(f"❌ API Error ({response.status_code}):", response.text)
        except Exception as e:
            print("❌ Exception occurred:", str(e))

# ==== Run Chat ====
if __name__ == "__main__":
    chat()
