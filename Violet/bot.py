import requests
import json

# ✅ Your OpenRouter API key
API_KEY = "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"

# ✅ DeepSeek model through OpenRouter
MODEL = "deepseek/deepseek-chat"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# ✅ Corrected headers (IMPORTANT: "Referer" not "HTTP-Referer")
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Referer": "http://localhost",   # ✅ Required by OpenRouter
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
            response = requests.post(API_URL, headers=HEADERS, json=payload)
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
