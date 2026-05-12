(function() {
    // --- Configuration ---
    // Change this to your production API URL if hosted remotely
    const API_URL = 'http://localhost:8088/api/v1/ask';

    // 1. Inject CSS for the widget
    const style = document.createElement('style');
    style.innerHTML = `
        #askhr-widget-container {
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 999999;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }
        #askhr-chat-button {
            background-color: #2563eb;
            color: white;
            border: none;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            font-size: 28px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: transform 0.2s;
        }
        #askhr-chat-button:hover {
            transform: scale(1.05);
        }
        #askhr-chat-window {
            display: none;
            flex-direction: column;
            width: 350px;
            height: 500px;
            background: #ffffff;
            border-radius: 12px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.2);
            overflow: hidden;
            margin-bottom: 16px;
            border: 1px solid #e5e7eb;
        }
        #askhr-chat-header {
            background: #2563eb;
            color: #ffffff;
            padding: 16px;
            font-weight: 600;
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 16px;
        }
        #askhr-close-btn {
            background: none;
            border: none;
            color: #ffffff;
            font-size: 24px;
            cursor: pointer;
            line-height: 1;
        }
        #askhr-chat-messages {
            flex: 1;
            padding: 16px;
            overflow-y: auto;
            background: #f9fafb;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .askhr-message {
            max-width: 85%;
            padding: 10px 14px;
            border-radius: 8px;
            font-size: 14px;
            line-height: 1.5;
            word-wrap: break-word;
        }
        .askhr-user-msg {
            background: #2563eb;
            color: #ffffff;
            align-self: flex-end;
            border-bottom-right-radius: 2px;
        }
        .askhr-bot-msg {
            background: #e5e7eb;
            color: #1f2937;
            align-self: flex-start;
            border-bottom-left-radius: 2px;
        }
        .askhr-sources {
            font-size: 11px;
            color: #4b5563;
            margin-top: 6px;
            font-style: italic;
            border-top: 1px solid #d1d5db;
            padding-top: 4px;
        }
        .askhr-loading {
            font-style: italic;
            color: #6b7280;
        }
        #askhr-chat-input-area {
            display: flex;
            padding: 12px;
            border-top: 1px solid #e5e7eb;
            background: #ffffff;
        }
        #askhr-chat-input {
            flex: 1;
            padding: 8px 12px;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            outline: none;
            font-size: 14px;
        }
        #askhr-chat-input:focus {
            border-color: #2563eb;
        }
        #askhr-send-btn {
            background: #2563eb;
            color: white;
            border: none;
            padding: 0 16px;
            margin-left: 8px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 500;
        }
        #askhr-send-btn:disabled {
            background: #9ca3af;
            cursor: not-allowed;
        }
    `;
    document.head.appendChild(style);

    // 2. Inject HTML for the widget
    const container = document.createElement('div');
    container.id = 'askhr-widget-container';
    container.innerHTML = `
        <div id="askhr-chat-window">
            <div id="askhr-chat-header">
                <span>HR Assistant</span>
                <button id="askhr-close-btn">&times;</button>
            </div>
            <div id="askhr-chat-messages">
                <div class="askhr-message askhr-bot-msg">Hello! I'm your virtual HR assistant. Ask me anything about our policies.</div>
            </div>
            <div id="askhr-chat-input-area">
                <input type="text" id="askhr-chat-input" placeholder="Type your question..." autocomplete="off" />
                <button id="askhr-send-btn">Send</button>
            </div>
        </div>
        <button id="askhr-chat-button">💬</button>
    `;
    document.body.appendChild(container);

    // 3. Connect Elements & Events
    const chatWindow = document.getElementById('askhr-chat-window');
    const chatButton = document.getElementById('askhr-chat-button');
    const closeBtn = document.getElementById('askhr-close-btn');
    const sendBtn = document.getElementById('askhr-send-btn');
    const inputField = document.getElementById('askhr-chat-input');
    const messagesContainer = document.getElementById('askhr-chat-messages');

    // Toggle Window
    chatButton.addEventListener('click', () => {
        chatWindow.style.display = chatWindow.style.display === 'flex' ? 'none' : 'flex';
        if (chatWindow.style.display === 'flex') inputField.focus();
    });
    
    closeBtn.addEventListener('click', () => {
        chatWindow.style.display = 'none';
    });

    // Helper: Add message to UI
    function appendMessage(text, isUser, sources = []) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `askhr-message ${isUser ? 'askhr-user-msg' : 'askhr-bot-msg'}`;
        msgDiv.textContent = text;
        
        if (sources && sources.length > 0) {
            const sourceDiv = document.createElement('div');
            sourceDiv.className = 'askhr-sources';
            sourceDiv.textContent = 'Sources: ' + sources.join(', ');
            msgDiv.appendChild(sourceDiv);
        }
        
        messagesContainer.appendChild(msgDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    // Main Chat Logic
    async function sendMessage() {
        const query = inputField.value.trim();
        if (!query) return;

        // 1. Show user message
        appendMessage(query, true);
        inputField.value = '';
        sendBtn.disabled = true;

        // 2. Show loading indicator
        const loadingId = 'loading-' + Date.now();
        const loadingDiv = document.createElement('div');
        loadingDiv.id = loadingId;
        loadingDiv.className = 'askhr-message askhr-bot-msg askhr-loading';
        loadingDiv.textContent = 'Searching policies...';
        messagesContainer.appendChild(loadingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;

        // 3. Call API
        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: query })
            });

            const data = await response.json();
            document.getElementById(loadingId).remove(); // Remove loading

            if (response.ok) {
                appendMessage(data.answer, false, data.sources);
            } else {
                appendMessage('Error: ' + (data.detail || 'Could not fetch response.'), false);
            }
        } catch (error) {
            document.getElementById(loadingId).remove();
            appendMessage('Connection failed. Make sure the AskHR API is running.', false);
            console.error('AskHR API Error:', error);
        } finally {
            sendBtn.disabled = false;
            inputField.focus();
        }
    }

    sendBtn.addEventListener('click', sendMessage);
    inputField.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendMessage();
    });

})();