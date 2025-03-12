from flask import Blueprint

# Create a Blueprint
chat = Blueprint('chat', __name__)

# Define your routes using the Blueprint
@chat.route('/chat')
def home():
    return 'Chat Page'