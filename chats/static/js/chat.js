document.addEventListener('DOMContentLoaded', () => {
    const socket = io();
    const messageInput = document.getElementById('message-input');
    const messageContainer = document.getElementById('message-container');

    socket.on('connect', () => {
        console.log('Connected to WebSocket server');
    });

    socket.on('message_history', (messages) => {
        messages.forEach(msg => appendMessage(msg));
    });

    socket.on('broadcast_message', (message) => {
        appendMessage(message);
    });

    window.sendMessage = () => {
        const text = messageInput.value.trim();
        if(text) {
            const timestamp = new Date().toISOString();
            socket.emit('new_message', {
                text: text,
                timestamp: timestamp
            });
            messageInput.value = '';
        }
    };

    let selectedUser = 'User1';

function selectUser(user) {
    selectedUser = user;
    document.getElementById('message-container').innerHTML = '';
}

function sendMessage() {
    const input = document.getElementById('message-input');
    const message = input.value;
    if (message.trim() === '') return;

    const timestamp = new Date().toISOString();
    const data = {
        text: message,
        timestamp: timestamp,
        sender: selectedUser
    };

    socket.emit('new_message', data);
    input.value = '';
}

function appendMessage(msg) {
        const messageElement = document.createElement('div');
        messageElement.className = 'message';
        messageElement.innerHTML = `
            <strong>${msg.sender}</strong>
            <p>${msg.text}</p>
            <small>${new Date(msg.timestamp).toLocaleTimeString()}</small>
        `;
        messageContainer.appendChild(messageElement);
        messageContainer.scrollTop = messageContainer.scrollHeight;
    }
});