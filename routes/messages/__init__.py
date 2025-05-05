from flask import Blueprint
from flask_socketio import SocketIO
from .routes import messages
from .conversation_route import conversation_route
from .chat_sockets import *
# Create a Blueprint for messages
messages_bp = Blueprint('messages', __name__)

messages_bp.register_blueprint(messages)
messages_bp.register_blueprint(conversation_route)

