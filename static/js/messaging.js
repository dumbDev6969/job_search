// Messaging module for handling real-time communication
const Messaging = {
    socket: null,
    currentChatUser: null,
    messageHistory: [],

    // Initialize the messaging system
    init() {
        this.socket = io();
        this.setupSocketListeners();
        this.setupUIHandlers();
    },

    // Set up Socket.IO event listeners
    setupSocketListeners() {
        this.socket.on('connect', () => {
            console.log('Connected to messaging server');
        });

        this.socket.on('new_message', (message) => {
            this.handleNewMessage(message);
        });

        this.socket.on('message_sent', (message) => {
            this.handleMessageSent(message);
        });

        this.socket.on('error', (error) => {
            console.error('Socket error:', error);
            this.showNotification(error.message, 'error');
        });
    },

    // Set up UI event handlers
    setupUIHandlers() {
        const messageForm = document.getElementById('message-form');
        const messageInput = document.getElementById('message-input');
        const userSearchInput = document.getElementById('user-search');

        if (messageForm) {
            messageForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.sendMessage(messageInput.value);
                messageInput.value = '';
            });
        }

        if (userSearchInput) {
            userSearchInput.addEventListener('input', debounce((e) => {
                this.searchUsers(e.target.value);
            }, 300));
        }
    },

    // Send a new message
    sendMessage(content) {
        if (!this.currentChatUser || !content.trim()) return;

        this.socket.emit('send_message', {
            receiver_id: this.currentChatUser.user_id,
            message: content.trim()
        });
    },

    // Load chat history with a user
    async loadChatHistory(userId) {
        try {
            const response = await fetch(`/api/messages/history/${userId}`);
            const data = await response.json();

            if (data.success) {
                this.messageHistory = data.messages;
                this.renderMessageHistory();
            } else {
                this.showNotification('Failed to load message history', 'error');
            }
        } catch (error) {
            console.error('Error loading chat history:', error);
            this.showNotification('Error loading chat history', 'error');
        }
    },

    // Search for users to chat with
    async searchUsers(searchTerm) {
        if (!searchTerm.trim()) {
            this.renderUserSearchResults([]);
            return;
        }

        try {
            const response = await fetch(`/api/messages/users/search?q=${encodeURIComponent(searchTerm)}`);
            const data = await response.json();

            if (data.success) {
                this.renderUserSearchResults(data.users);
            }
        } catch (error) {
            console.error('Error searching users:', error);
        }
    },

    // Handle incoming new message
    handleNewMessage(message) {
        if (this.currentChatUser && message.sender_id === this.currentChatUser.user_id) {
            this.messageHistory.unshift(message);
            this.renderMessageHistory();
        }
        this.showNotification('New message received', 'info');
    },

    // Handle successful message sending
    handleMessageSent(message) {
        this.messageHistory.unshift(message);
        this.renderMessageHistory();
    },

    // Render message history in the UI
    renderMessageHistory() {
        const chatContainer = document.getElementById('chat-messages');
        if (!chatContainer) return;

        chatContainer.innerHTML = this.messageHistory
            .map(msg => this.createMessageElement(msg))
            .join('');

        chatContainer.scrollTop = chatContainer.scrollHeight;
    },

    // Create HTML element for a message
    createMessageElement(message) {
        const isOutgoing = message.type === 'sent';
        return `
            <div class="message ${isOutgoing ? 'outgoing' : 'incoming'}">
                <div class="message-content">
                    <p>${this.escapeHtml(message.content)}</p>
                    <span class="message-time">${this.formatTime(message.sent_at)}</span>
                </div>
            </div>
        `;
    },

    // Render user search results
    renderUserSearchResults(users) {
        const resultsContainer = document.getElementById('search-results');
        if (!resultsContainer) return;

        resultsContainer.innerHTML = users
            .map(user => `
                <div class="user-result" onclick="Messaging.startChat(${JSON.stringify(user)})">
                    <span class="user-name">${this.escapeHtml(user.display_name)}</span>
                    <span class="user-type">${this.escapeHtml(user.user_type)}</span>
                </div>
            `)
            .join('');
    },

    // Start a chat with a user
    startChat(user) {
        this.currentChatUser = user;
        this.loadChatHistory(user.user_id);
        
        const chatHeader = document.getElementById('chat-header');
        if (chatHeader) {
            chatHeader.textContent = `Chat with ${user.display_name}`;
        }
    },

    // Show notification
    showNotification(message, type = 'info') {
        // Implement your preferred notification system
        console.log(`${type.toUpperCase()}: ${message}`);
    },

    // Helper function to format time
    formatTime(timestamp) {
        return new Date(timestamp).toLocaleTimeString();
    },

    // Helper function to escape HTML
    escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }
};

// Debounce helper function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
};

// Initialize messaging when the document is ready
document.addEventListener('DOMContentLoaded', () => {
    Messaging.init();
});