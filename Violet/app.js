// let prevScrollPos = window.pageYOffset;
// const navbar = document.getElementById("navbar");
// let navbarHeight = navbar.offsetHeight;

// window.onscroll = function () {
//   let currentScrollPos = window.pageYOffset;

//   if (prevScrollPos > currentScrollPos) {
//     navbar.style.top = "0";
//   } else {
//     navbar.style.top = `-${navbarHeight}px`;
//   }

//   prevScrollPos = currentScrollPos;
// };

// //chatbox
// const chatIcon = document.getElementById("chat-icon");
// const chatBox = document.getElementById("chat-box");
// const closeChat = document.getElementById("close-chat");
// const sendMessage = document.getElementById("send-message");
// const chatMessage = document.getElementById("chat-message");
// const chatMessages = document.querySelector(".chat-messages");

// chatIcon.addEventListener("click", () => {
//   chatBox.classList.remove("hidden");
// });

// closeChat.addEventListener("click", () => {
//   chatBox.classList.add("hidden");
// });

// sendMessage.addEventListener("click", sendChatMessage);
// chatMessage.addEventListener("keypress", (e) => {
//   if (e.key === "Enter") {
//     sendChatMessage();
//   }
// });

// function sendChatMessage() {
//   const message = chatMessage.value.trim();
//   if (message) {
//     const messageElement = document.createElement("div");
//     messageElement.textContent = `You: ${message}`;
//     chatMessages.appendChild(messageElement);
//     chatMessage.value = "";
//     chatMessages.scrollTop = chatMessages.scrollHeight;

//     //for response
//     setTimeout(() => {
//       const responseElement = document.createElement("div");
//       responseElement.textContent = `Amethyst: Thanks for your message! We'll get back to you soon.`;
//       chatMessages.appendChild(responseElement);
//       chatMessages.scrollTop = chatMessages.scrollHeight;
//     }, 800);
//   }
// }

const chatIcon = document.getElementById("chat-icon");
const chatBox = document.getElementById("chat-box");
const closeChat = document.getElementById("close-chat");
const chatMessages = document.querySelector(".chat-messages");
const chatInput = document.getElementById("chat-message");
const sendMessage = document.getElementById("send-message");

chatIcon.addEventListener("click", () => {
  chatBox.classList.remove("hidden");
});

closeChat.addEventListener("click", () => {
  chatBox.classList.add("hidden");
});

async function sendToDeepSeek(message) {
  const response = await fetch("https://openrouter.ai/api/v1/chat/completions", {
    method: "POST",
    headers: {
      "Authorization": "Bearer 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",
      "Content-Type": "application/json",
      "HTTP-Referer": "http://localhost",
      "X-Title": "Violet Chatbot"
    },
    body: JSON.stringify({
      model: "deepseek/deepseek-chat",
      messages: [{ role: "user", content: message }]
    })
  });

  const data = await response.json();
  return data.choices?.[0]?.message?.content || "Sorry, I couldn't understand that.";
}

function addMessage(content, sender) {
  const msg = document.createElement("div");
  msg.textContent = content;
  msg.style.marginBottom = "10px";
  msg.style.background = sender === "user" ? "#f4d9f7" : "#e0e0ff";
  msg.style.padding = "8px";
  msg.style.borderRadius = "5px";
  msg.style.alignSelf = sender === "user" ? "flex-end" : "flex-start";
  chatMessages.appendChild(msg);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

sendMessage.addEventListener("click", async () => {
  const userMsg = chatInput.value.trim();
  if (!userMsg) return;

  addMessage(userMsg, "user");
  chatInput.value = "";

  const reply = await sendToDeepSeek(userMsg);
  addMessage(reply, "bot");
});

chatInput.addEventListener("keypress", async (e) => {
  if (e.key === "Enter") {
    sendMessage.click();
  }
});
