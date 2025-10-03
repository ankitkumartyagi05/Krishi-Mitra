// Chat Module
let chatHistory = [];
let isRecording = false;
let recognition = null;

// DOM Elements
const chatMessages = document.getElementById('chat-messages');
const messageInput = document.getElementById('message-input');
const sendMessageBtn = document.getElementById('send-message-btn');
const voiceInputBtn = document.getElementById('voice-input-btn');
const imageInputBtn = document.getElementById('image-input-btn');
const videoInputBtn = document.getElementById('video-input-btn');
const chatHistoryContainer = document.getElementById('chat-history');

// Initialize Chat Module
function initializeChat() {
    // Event listeners
    sendMessageBtn.addEventListener('click', sendMessage);
    messageInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
    
    voiceInputBtn.addEventListener('click', toggleVoiceInput);
    imageInputBtn.addEventListener('click', () => {
        document.createElement('input').type = 'file';
        document.createElement('input').accept = 'image/*';
        document.createElement('input').click();
    });
    
    videoInputBtn.addEventListener('click', () => {
        document.createElement('input').type = 'file';
        document.createElement('input').accept = 'video/*';
        document.createElement('input').click();
    });
    
    // Initialize speech recognition if available
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        recognition = new SpeechRecognition();
        recognition.continuous = false;
        recognition.interimResults = false;
        recognition.lang = 'en-US';
        
        recognition.onresult = (event) => {
            const transcript = event.results[0][0].transcript;
            messageInput.value = transcript;
            sendMessage();
        };
        
        recognition.onerror = (event) => {
            console.error('Speech recognition error:', event.error);
            showNotification('Speech recognition error: ' + event.error, 'error');
            isRecording = false;
            updateVoiceButton();
        };
        
        recognition.onend = () => {
            isRecording = false;
            updateVoiceButton();
        };
    } else {
        voiceInputBtn.style.display = 'none';
    }
    
    // Load chat history
    loadChatHistory();
    
    // Add click handlers to message options
    document.addEventListener('click', (e) => {
        if (e.target.classList.contains('message-option')) {
            messageInput.value = e.target.textContent;
            sendMessage();
        }
    });
}

// Send Message
function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;
    
    // Add user message to chat
    addUserMessage(message);
    
    // Clear input
    messageInput.value = '';
    
    // Send to backend and get response
    getBotResponse(message);
    
    // Save to history
    saveToChatHistory('user', message);
}

// Add User Message
function addUserMessage(message) {
    const messageElement = document.createElement('div');
    messageElement.className = 'message user-message';
    messageElement.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-user"></i>
        </div>
        <div class="message-content">
            <p>${escapeHtml(message)}</p>
        </div>
    `;
    
    chatMessages.appendChild(messageElement);
    scrollToBottom();
}

// Add Bot Message
function addBotMessage(message, options = null) {
    const messageElement = document.createElement('div');
    messageElement.className = 'message bot-message';
    
    let messageContent = `<p>${escapeHtml(message)}</p>`;
    
    if (options && options.length > 0) {
        messageContent += '<div class="message-options">';
        options.forEach(option => {
            messageContent += `<button class="message-option">${escapeHtml(option)}</button>`;
        });
        messageContent += '</div>';
    }
    
    messageElement.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
            ${messageContent}
        </div>
    `;
    
    chatMessages.appendChild(messageElement);
    scrollToBottom();
    
    // Save to history
    saveToChatHistory('bot', message);
}

// Get Bot Response
function getBotResponse(message) {
    // Show typing indicator
    showTypingIndicator();
    
    // In a real implementation, you would send to your backend API
    // For demo purposes, we'll simulate responses
    setTimeout(() => {
        removeTypingIndicator();
        
        const lowerMessage = message.toLowerCase();
        let response = '';
        let options = [];
        
        if (lowerMessage.includes('weather') || lowerMessage.includes('rain')) {
            response = 'The weather forecast for your location shows partly cloudy skies with a 30% chance of rain tomorrow. Temperature will be around 28°C.';
            options = ['5-day forecast', 'Weather alerts', 'Historical data'];
        } else if (lowerMessage.includes('price') || lowerMessage.includes('market')) {
            response = 'Current market price for wheat in Punjab is ₹2100 per quintal, which is ₹50 higher than last week.';
            options = ['Price trends', 'Other crops', 'Price prediction'];
        } else if (lowerMessage.includes('soil') || lowerMessage.includes('fertilizer')) {
            response = 'Based on your soil analysis, I recommend applying urea at 50kg/ha and DAP at 25kg/ha for better crop yield.';
            options = ['Soil test', 'Crop recommendations', 'Organic farming'];
        } else if (lowerMessage.includes('pest') || lowerMessage.includes('disease')) {
            response = 'For pest control, I recommend using neem oil spray as an organic solution. If the infestation is severe, consult an agricultural expert.';
            options = ['Upload pest image', 'Common pests', 'Prevention tips'];
        } else if (lowerMessage.includes('crop') || lowerMessage.includes('sowing')) {
            response = 'The best time for sowing wheat in your region is from October to November. Make sure soil moisture is adequate.';
            options = ['Crop calendar', 'Seed varieties', 'Irrigation schedule'];
        } else {
            response = 'I can help you with weather updates, market prices, soil health, pest control, and crop advice. What would you like to know?';
            options = ['Weather Update', 'Market Prices', 'Crop Advice', 'Pest Control'];
        }
        
        addBotMessage(response, options);
    }, 1500);
}

// Show Typing Indicator
function showTypingIndicator() {
    const indicator = document.createElement('div');
    indicator.className = 'message bot-message typing-indicator';
    indicator.id = 'typing-indicator';
    indicator.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-robot"></i>
        </div>
        <div class="message-content">
            <div class="typing-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        </div>
    `;
    
    chatMessages.appendChild(indicator);
    scrollToBottom();
}

// Remove Typing Indicator
function removeTypingIndicator() {
    const indicator = document.getElementById('typing-indicator');
    if (indicator) {
        indicator.remove();
    }
}

// Toggle Voice Input
function toggleVoiceInput() {
    if (!recognition) return;
    
    if (isRecording) {
        recognition.stop();
    } else {
        recognition.start();
        isRecording = true;
        updateVoiceButton();
    }
}

// Update Voice Button
function updateVoiceButton() {
    if (isRecording) {
        voiceInputBtn.innerHTML = '<i class="fas fa-stop"></i>';
        voiceInputBtn.style.backgroundColor = '#F44336';
    } else {
        voiceInputBtn.innerHTML = '<i class="fas fa-microphone"></i>';
        voiceInputBtn.style.backgroundColor = '';
    }
}

// Scroll to Bottom
function scrollToBottom() {
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Save to Chat History
function saveToChatHistory(sender, message) {
    const timestamp = new Date().toISOString();
    chatHistory.push({ sender, message, timestamp });
    
    // Update history display
    updateChatHistoryDisplay();
    
    // Save to localStorage
    localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
}

// Load Chat History
function loadChatHistory() {
    const savedHistory = localStorage.getItem('chatHistory');
    if (savedHistory) {
        chatHistory = JSON.parse(savedHistory);
        updateChatHistoryDisplay();
    }
}

// Update Chat History Display
function updateChatHistoryDisplay() {
    chatHistoryContainer.innerHTML = '';
    
    // Show last 5 conversations
    const recentHistory = chatHistory.slice(-5);
    
    recentHistory.forEach((item, index) => {
        if (item.sender === 'user') {
            const historyItem = document.createElement('div');
            historyItem.className = 'history-item';
            historyItem.textContent = item.message.substring(0, 30) + (item.message.length > 30 ? '...' : '');
            historyItem.addEventListener('click', () => {
                loadConversation(index);
            });
            chatHistoryContainer.appendChild(historyItem);
        }
    });
}

// Load Conversation
function loadConversation(startIndex) {
    // Clear current messages
    chatMessages.innerHTML = '';
    
    // Add welcome message
    addBotMessage('Hello! I\'m your KrishiMitra assistant. How can I help you today?', [
        'Weather Update',
        'Market Prices',
        'Crop Advice',
        'Pest Control'
    ]);
    
    // Load messages from history
    for (let i = startIndex; i < chatHistory.length; i++) {
        const item = chatHistory[i];
        if (item.sender === 'user') {
            addUserMessage(item.message);
        } else {
            addBotMessage(item.message);
        }
    }
}

// Utility Functions
function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    
    return text.replace(/[&<>"']/g, m => map[m]);
}

// Add typing indicator styles
const typingStyles = document.createElement('style');
typingStyles.textContent = `
    .typing-dots {
        display: flex;
        align-items: center;
    }
    
    .typing-dots span {
        width: 8px;
        height: 8px;
        margin: 0 2px;
        background-color: #757575;
        border-radius: 50%;
        animation: typing 1.4s infinite;
    }
    
    .typing-dots span:nth-child(2) {
        animation-delay: 0.2s;
    }
    
    .typing-dots span:nth-child(3) {
        animation-delay: 0.4s;
    }
    
    @keyframes typing {
        0%, 60%, 100% {
            transform: translateY(0);
        }
        30% {
            transform: translateY(-10px);
        }
    }
`;
document.head.appendChild(typingStyles);