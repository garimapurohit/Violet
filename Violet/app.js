const chatIcon = document.getElementById("chat-icon");
const chatBox = document.getElementById("chat-box");
const closeChat = document.getElementById("close-chat");
const sendMessageBtn = document.getElementById("send-message");
const chatMessages = document.querySelector(".chat-messages");
const chatInput = document.getElementById("chat-message");

// State
let messages = [];

// Show chat window
chatIcon.addEventListener("click", () => {
  chatBox.classList.remove("hidden");
  chatInput.focus();
});

// Close chat window
closeChat.addEventListener("click", () => {
  chatBox.classList.add("hidden");
});

// Send user message
sendMessageBtn.addEventListener("click", () => {
  const userText = chatInput.value.trim();
  if (!userText) return;

  appendMessage("user", userText);
  chatInput.value = "";
  sendToBackend(userText);
});

// Send on Enter key
chatInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    e.preventDefault();
    sendMessageBtn.click();
  }
});

// Append message to chat box
function appendMessage(role, content) {
  const message = document.createElement("div");
  message.classList.add("message", role);
  message.innerText = content;
  chatMessages.appendChild(message);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Send message to backend server
function sendToBackend(userMessage) {
  messages.push({ role: "user", content: userMessage });

  fetch("http://localhost:5000/api/chat", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ messages: messages })
  })
    .then((res) => {
      if (!res.ok) throw new Error("API request failed");
      return res.json();
    })
    .then((data) => {
      const reply = data.reply;
      messages.push({ role: "assistant", content: reply });
      appendMessage("assistant", reply);
    })
    .catch((err) => {
      console.error(err);
      appendMessage("assistant", "⚠️ Oops! Something went wrong.");
    });
}


