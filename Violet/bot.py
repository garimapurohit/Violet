import requests
import json

API_KEY = "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"
MODEL = "deepseek/deepseek-chat"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Referer": "http://localhost",  # Correct header name
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
            response = requests.post(API_URL, headers=HEADERS, data=json.dumps(payload), timeout=30)
            
            if response.status_code == 200:
                reply = response.json()["choices"][0]["message"]["content"].strip()
                print("Assistant:", reply)
                messages.append({"role": "assistant", "content": reply})
            else:
                print(f"❌ API Error {response.status_code}: {response.reason}")
                print("Response Body:", response.text)

        except Exception as e:
            print("❌ Exception occurred:", str(e))

# ==== Run Chat ====
if __name__ == "__main__":
    chat()
