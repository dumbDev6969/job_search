from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

active_users = set()

import json
import os

# Message storage setup
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
MESSAGES_FILE = os.path.join(DATA_DIR, 'messages.json')

# Create data directory if needed
os.makedirs(DATA_DIR, exist_ok=True)

# Load existing messages
try:
    with open(MESSAGES_FILE, 'r') as f:
        messages = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    messages = []

@socketio.on('connect')
def handle_connect():
    user_id = f'User{len(active_users) + 1}'
    active_users.add(user_id)
    emit('message_history', messages)
    emit('update_users', list(active_users), broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    user_id = next(iter(active_users), None)
    if user_id:
        active_users.discard(user_id)
        emit('update_users', list(active_users), broadcast=True)

@socketio.on('new_message')
def handle_message(data):
    message = {
        'text': data['text'],
        'timestamp': data['timestamp'],
        'sender': 'User' + str(len(messages)+1)
    }
    messages.append(message)
    # Save to file
    with open(MESSAGES_FILE, 'w') as f:
        json.dump(messages, f)
    
    emit('broadcast_message', message, broadcast=True)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, debug=True)