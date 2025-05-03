from flask import Blueprint, render_template, session, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
from utils.database import get_db
from middlewares.verify_user import verify_user_socket  # Make sure this exists
from sqlalchemy import text
from datetime import datetime

def chat(socketio):

    # Socket.IO Events (Keep database logic unchanged)
    @socketio.on('connect')
    def handle_connect():
        user_id = session.get('user_id')
        if not user_id:
            return False
        join_room(f"user_{user_id}")
        print(f"User {user_id} connected")

    @socketio.on('disconnect')
    def handle_disconnect():
        user_id = session.get('user_id')
        if user_id:
            leave_room(f"user_{user_id}")
        print(f"User {user_id} disconnected")

    @socketio.on('send_message')
    def handle_send_message(data):
        user_id = session.get('user_id')
        if not user_id:
            emit('error', {'message': 'Not authenticated'})
            return

        receiver_id = data.get('receiver_id')
        content = data.get('message')
        
        if not receiver_id or not content:
            emit('error', {'message': 'Invalid message data'})
            return

        db = get_db()
        query = text("""
            INSERT INTO messages (sender_id, receiver_id, content, sent_at)
            VALUES (:sender_id, :receiver_id, :content, :sent_at)
        """)
        result = db.execute_query(query, {
            'sender_id': user_id,
            'receiver_id': receiver_id,
            'content': content,
            'sent_at': datetime.utcnow()
        })
        
        if not result['success']:
            emit('error', {'message': 'Failed to send message'})
            return

        # Get the message for response
        message_data = {
            'sender_id': user_id,
            'receiver_id': receiver_id,
            'content': content,
            'sent_at': datetime.utcnow().isoformat(),
            'type': 'sent'
        }
        
        # Emit to both users
        emit('receive_message', message_data, room=f"user_{user_id}")
        emit('receive_message', message_data, room=f"user_{receiver_id}")
        emit('status', {'status': 'sent'})

    @socketio.on('load_conversation')
    def handle_load_conversation(data):
        user_id = session.get('user_id')
        other_user_id = data.get('other_user_id')
        
        if not user_id or not other_user_id:
            emit('error', {'message': 'Missing user ID'})
            return

        db = get_db()
        query = text("""
            SELECT m.*, 
                CASE WHEN m.sender_id = :user_id THEN 'sent' ELSE 'received' END as message_type
            FROM messages m
            WHERE (m.sender_id = :user_id AND m.receiver_id = :other_user_id)
            OR (m.sender_id = :other_user_id AND m.receiver_id = :user_id)
            ORDER BY m.sent_at ASC
        """)
        result = db.execute_query(query, {'user_id': user_id, 'other_user_id': other_user_id})
        
        if result['success']:
            emit('conversation_loaded', result['output'])
        else:
            emit('error', {'message': 'Failed to load conversation'})

    @socketio.on('search_users')
    def handle_search_users(data):
        user_id = session.get('user_id')
        search_term = data.get('query', '').strip()
        
        db = get_db()
        query = text("""
            SELECT 
                js.seeker_id as user_id,
                js.email,
                'job_seeker' as user_type,
                CONCAT(js.first_name, ' ', js.last_name) as display_name
            FROM job_seekers js
            WHERE LOWER(CONCAT(js.first_name, ' ', js.last_name)) LIKE :search_pattern
                OR LOWER(js.email) LIKE :search_pattern
            UNION ALL
            SELECT 
                e.employer_id as user_id,
                e.email,
                'employer' as user_type,
                e.company_name as display_name
            FROM employers e
            WHERE LOWER(e.company_name) LIKE :search_pattern
                OR LOWER(e.email) LIKE :search_pattern
        """)
        result = db.execute_query(query, {
            'search_pattern': f'%{search_term.lower()}%'
        })
        
        if result['success']:
            emit('user_search_results', result['output'])
        else:
            emit('user_search_results', [])

    @socketio.on('get_chat_partners')
    def handle_get_chat_partners():
        user_id = session.get('user_id')
        if not user_id:
            emit('error', {'message': 'Not authenticated'})
            return
        
        db = get_db()
        query = text("""
            SELECT DISTINCT 
                CASE WHEN sender_id = :user_id THEN receiver_id ELSE sender_id END as partner_id,
                CASE WHEN sender_id = :user_id THEN 'sent' ELSE 'received' END as direction
            FROM messages
            WHERE sender_id = :user_id OR receiver_id = :user_id
            ORDER BY direction DESC
        """)
        result = db.execute_query(query, {'user_id': user_id})
        
        if not result['success'] or not result['output']:
            emit('chat_partners', [])
            return
        
        partners = []
        for partner in result['output']:
            partner_id = partner['partner_id']
            query = text("""
                SELECT 
                    js.seeker_id as user_id,
                    js.email,
                    'job_seeker' as user_type,
                    CONCAT(js.first_name, ' ', js.last_name) as display_name
                FROM job_seekers js
                WHERE js.seeker_id = :user_id 
                UNION ALL
                SELECT 
                    e.employer_id as user_id,
                    e.email,
                    'employer' as user_type,
                    e.company_name as display_name
                FROM employers e
                WHERE e.employer_id = :user_id
            """)
            user_result = db.execute_query(query, {'user_id': partner_id})
            
            if user_result['success'] and user_result['output']:
                partners.extend(user_result['output'])
        
        emit('chat_partners', partners)