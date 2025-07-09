document.addEventListener('DOMContentLoaded', function() {
  // Get all elements
  const chatIcon = document.getElementById("chat-icon");
  const chatBox = document.getElementById("chat-box");
  const closeChat = document.getElementById("close-chat");
  const sendBtn = document.getElementById("send-message");
  const chatInput = document.getElementById("chat-message");
  const chatMessages = document.querySelector(".chat-messages");

  // Toggle chat visibility
  chatIcon.addEventListener('click', function() {
    chatBox.classList.remove("hidden");
    chatInput.focus();
  });

  closeChat.addEventListener('click', function() {
    chatBox.classList.add("hidden");
  });

  // Send message function
  function sendMessage() {
    const message = chatInput.value.trim();
    if (!message) return;

    // Add user message
    addMessage('user', message);
    chatInput.value = '';

    // Add temporary bot message
    const botMessage = addMessage('assistant', '...');

    // Send to backend
    fetch('http://127.0.0.1:5000/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        messages: [{ role: 'user', content: message }]
      })
    })
    .then(response => response.json())
    .then(data => {
      // Update bot message
      botMessage.textContent = data.success ? data.message : `Error: ${data.error}`;
    })
    .catch(error => {
      botMessage.textContent = "Sorry, I can't connect right now";
      console.error('Error:', error);
    });
  }

  // Helper to add messages
  function addMessage(sender, text) {
    const div = document.createElement('div');
    div.className = `message ${sender}`;
    div.textContent = text;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return div;
  }

  // Event listeners
  sendBtn.addEventListener('click', sendMessage);
  chatInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') sendMessage();
  });
});