function initChatBot() {
  const chatbotElement = document.getElementById('chatbot');
  if (!chatbotElement) return;

  chatbotElement.innerHTML = `
    <button class="chat-toggle" id="chatToggle">💬</button>
    <div class="chat-window" id="chatWindow" style="display:none;">
      <div class="chat-header">
        <span>ECOSYNTH Support</span>
        <button onclick="document.getElementById('chatWindow').style.display='none'">-</button>
      </div>
      <div class="chat-messages" id="chatMessages">
        <div class="bot-message">${chatbotData.welcomeMessage}</div>
      </div>
      <div class="chat-input">
        <input type="text" id="userInput" placeholder="Type a message" />
        <button onclick="sendMessage()">Send</button>
      </div>
    </div>
  `;

  document.getElementById('chatToggle').addEventListener('click', () => {
    const chatWindow = document.getElementById('chatWindow');
    chatWindow.style.display = chatWindow.style.display === 'none' ? 'flex' : 'none';
  });
}

function sendMessage() {
  const inputField = document.getElementById('userInput');
  const message = inputField.value.trim();
  if (message === '') return;

  const chatMessages = document.getElementById('chatMessages');

  const userMessage = document.createElement('div');
  userMessage.className = 'user-message';
  userMessage.textContent = message;
  chatMessages.appendChild(userMessage);

  const response = generateResponse(message);

  const botMessage = document.createElement('div');
  botMessage.className = 'bot-message';
  botMessage.textContent = response;
  chatMessages.appendChild(botMessage);

  inputField.value = '';
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function generateResponse(input) {
  const lowerInput = input.toLowerCase();

  // Greetings
  if (["hi", "hello", "helo", "hy"].includes(lowerInput)) {
    return chatbotData.greetings[0];
  } else if (lowerInput.includes("good morning")) {
    return chatbotData.greetings[2];
  } else if (lowerInput.includes("good afternoon")) {
    return chatbotData.greetings[3];
  } else if (lowerInput.includes("good evening")) {
    return chatbotData.greetings[4];
  } else if (lowerInput.includes("good night")) {
    return chatbotData.greetings[5];
  }

  // Match known questions
  for (let item of chatbotData.commonQuestions) {
    if (lowerInput.includes(item.question.toLowerCase().slice(0, 12))) {
      return item.answer;
    }
  }

  // Fallback response
  const fallbackIndex = Math.floor(Math.random() * chatbotData.fallbackResponses.length);
  return chatbotData.fallbackResponses[fallbackIndex];
}
