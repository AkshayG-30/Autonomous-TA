/**
 * Autonomous Lab TA - Debug Interface JavaScript
 * Handles API communication for testing the backend
 */

const API_BASE = '/api';  // Relative URL since frontend is served from same server

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

// Modal Elements
const modal = document.getElementById('source-modal');
const modalContent = document.getElementById('modal-content');
const modalTitle = document.getElementById('modal-title');
const modalCategory = document.getElementById('modal-category');
const modalContentText = document.getElementById('modal-content-text');
const modalClose = document.getElementById('modal-close');
const modalMinimize = document.getElementById('modal-minimize');
const modalMaximize = document.getElementById('modal-maximize');

// Check API Connection
async function checkAPIStatus() {
    try {
        const response = await fetch('/health');
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

        // Add TA response with sources
        addChatMessage(result.response, 'ta', result.sources);

    } catch (error) {
        document.getElementById('typing-indicator')?.remove();
        addChatMessage(`Error connecting to TA: ${error.message}. Make sure the backend is running.`, 'ta');
    }
}

// Add message to chat
function addChatMessage(text, sender, sources = []) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;

    if (sender === 'ta') {
        let html = `<strong>TA:</strong> ${formatMessage(text)}`;

        // Add source references if available
        if (sources && sources.length > 0) {
            html += `
                <div class="source-references">
                    <div class="source-references-title">📚 Referenced Materials:</div>
                    <div class="source-links">
                        ${sources.map(src => `
                            <span class="source-link" onclick="openSourceModal('${src.name}')" title="${src.snippet || 'Click to view'}">
                                <span class="source-link-icon">📄</span>
                                ${src.name}
                            </span>
                        `).join('')}
                    </div>
                </div>
            `;
        }

        messageDiv.innerHTML = html;
    } else {
        messageDiv.innerHTML = `<strong>You:</strong> ${text}`;
    }

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Format message using marked.js for full Markdown support
function formatMessage(text) {
    // Use marked.js if available, otherwise fallback to basic formatting
    if (typeof marked !== 'undefined') {
        // Configure marked for safe rendering
        marked.setOptions({
            breaks: true,  // Convert line breaks to <br>
            gfm: true,     // GitHub Flavored Markdown
            sanitize: false
        });
        return marked.parse(text);
    }

    // Fallback if marked.js not loaded
    return text
        .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
        .replace(/```(\w*)\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>')
        .replace(/`([^`]+)`/g, '<code>$1</code>')
        .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" class="external-link">$1 ↗</a>')
        .replace(/\n/g, '<br>');
}

// Open source modal with rendered Markdown
async function openSourceModal(filename) {
    try {
        // Show loading state
        modal.classList.add('active');
        modalTitle.textContent = filename.replace('.md', '');
        modalCategory.textContent = 'Loading...';
        modalContentText.innerHTML = '<div class="loading-spinner">📖 Loading content...</div>';

        // Fetch file content
        const response = await fetch(`${API_BASE}/chat/knowledge/${encodeURIComponent(filename)}`);

        if (!response.ok) {
            throw new Error('File not found');
        }

        const data = await response.json();

        // Update modal title with friendly name
        const friendlyName = data.name.replace('.md', '').replace(/_/g, ' ');
        modalTitle.textContent = friendlyName.charAt(0).toUpperCase() + friendlyName.slice(1);
        modalCategory.textContent = data.category;

        // Render Markdown as HTML for learner-friendly display
        if (typeof marked !== 'undefined') {
            marked.setOptions({
                breaks: true,
                gfm: true,
                highlight: function (code, lang) {
                    return `<code class="language-${lang}">${code}</code>`;
                }
            });
            modalContentText.innerHTML = marked.parse(data.content);
        } else {
            // Fallback: show as text
            modalContentText.textContent = data.content;
        }

    } catch (error) {
        modalContentText.innerHTML = `<div class="error-message">❌ Error loading file: ${error.message}</div>`;
        modalCategory.textContent = 'Error';
    }
}

// Close modal
function closeModal() {
    modal.classList.remove('active');
    modalContent.classList.remove('maximized', 'minimized');
}

// Minimize modal
function minimizeModal() {
    modalContent.classList.toggle('minimized');
    modalContent.classList.remove('maximized');
}

// Maximize modal
function maximizeModal() {
    modalContent.classList.toggle('maximized');
    modalContent.classList.remove('minimized');
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

// Modal event listeners
modalClose.addEventListener('click', closeModal);
modalMinimize.addEventListener('click', minimizeModal);
modalMaximize.addEventListener('click', maximizeModal);

// Close modal when clicking outside
modal.addEventListener('click', (e) => {
    if (e.target === modal) {
        closeModal();
    }
});

// Close modal with Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('active')) {
        closeModal();
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

