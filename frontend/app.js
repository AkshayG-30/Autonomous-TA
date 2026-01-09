/**
 * Autonomous Lab TA - Debug Interface JavaScript
 * Handles API communication for testing the backend
 */

const API_BASE = 'http://localhost:8000/api';

// DOM Elements
const codeEditor = document.getElementById('code-editor');
const languageSelect = document.getElementById('language-select');
const runBtn = document.getElementById('run-btn');
const clearBtn = document.getElementById('clear-btn');
const outputArea = document.getElementById('output-area');
const executionStatus = document.getElementById('execution-status');
const chatMessages = document.getElementById('chat-messages');
const chatInput = document.getElementById('chat-input');
const sendBtn = document.getElementById('send-btn');
const apiStatus = document.getElementById('api-status');

// Check API Connection
async function checkAPIStatus() {
    try {
        const response = await fetch('http://localhost:8000/health');
        if (response.ok) {
            apiStatus.textContent = 'Connected';
            apiStatus.className = 'status-indicator connected';
        } else {
            throw new Error('API not responding');
        }
    } catch (error) {
        apiStatus.textContent = 'Disconnected';
        apiStatus.className = 'status-indicator disconnected';
    }
}

// Run Code
async function runCode() {
    const code = codeEditor.value;
    const language = languageSelect.value;

    if (!code.trim()) {
        outputArea.textContent = 'Please enter some code to run.';
        return;
    }

    // Show running status
    executionStatus.textContent = 'Running...';
    executionStatus.className = 'status running';
    outputArea.textContent = 'Executing code...';
    runBtn.disabled = true;

    try {
        const response = await fetch(`${API_BASE}/submissions/run`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                code: code,
                language: language
            })
        });

        const result = await response.json();

        if (result.success) {
            executionStatus.textContent = 'Success';
            executionStatus.className = 'status success';
            outputArea.textContent = result.output || '(No output)';
        } else {
            executionStatus.textContent = 'Error';
            executionStatus.className = 'status error';
            outputArea.textContent = result.error || result.output || 'Execution failed';
        }

        if (result.execution_time) {
            executionStatus.textContent += ` (${result.execution_time.toFixed(2)}s)`;
        }

    } catch (error) {
        executionStatus.textContent = 'Error';
        executionStatus.className = 'status error';
        outputArea.textContent = `Failed to connect to API: ${error.message}\n\nMake sure the backend is running:\ncd backend && uvicorn main:app --reload`;
    } finally {
        runBtn.disabled = false;
    }
}

// Send Chat Message
async function sendMessage() {
    const message = chatInput.value.trim();
    const code = codeEditor.value;

    if (!message) return;

    // Add user message to chat
    addChatMessage(message, 'user');
    chatInput.value = '';

    // Add typing indicator
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message ta-message';
    typingDiv.id = 'typing-indicator';
    typingDiv.innerHTML = '<strong>TA:</strong> <span class="loading"></span> Thinking...';
    chatMessages.appendChild(typingDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    try {
        const response = await fetch(`${API_BASE}/chat/ask`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                message: message,
                code: code
            })
        });

        const result = await response.json();

        // Remove typing indicator
        document.getElementById('typing-indicator')?.remove();

        // Add TA response
        addChatMessage(result.response, 'ta');

    } catch (error) {
        document.getElementById('typing-indicator')?.remove();
        addChatMessage(`Error connecting to TA: ${error.message}. Make sure the backend is running.`, 'ta');
    }
}

// Add message to chat
function addChatMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;

    if (sender === 'ta') {
        messageDiv.innerHTML = `<strong>TA:</strong> ${formatMessage(text)}`;
    } else {
        messageDiv.innerHTML = `<strong>You:</strong> ${text}`;
    }

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Format message (basic markdown-like formatting)
function formatMessage(text) {
    return text
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        .replace(/\n/g, '<br>');
}

// Clear editor
function clearEditor() {
    codeEditor.value = '';
    outputArea.textContent = 'Output will appear here...';
    executionStatus.textContent = '';
    executionStatus.className = 'status';
}

// Event Listeners
runBtn.addEventListener('click', runCode);
clearBtn.addEventListener('click', clearEditor);
sendBtn.addEventListener('click', sendMessage);

chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Keyboard shortcut: Ctrl+Enter to run code
codeEditor.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 'Enter') {
        runCode();
    }
});

// Initial API check
checkAPIStatus();
setInterval(checkAPIStatus, 5000);

// Sample code
codeEditor.value = `# Sample Python Code
# Press Ctrl+Enter or click "Run Code" to execute

def greet(name):
    return f"Hello, {name}!"

for i in range(3):
    print(greet(f"Student {i+1}"))
`;
