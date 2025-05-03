from flask import Blueprint, render_template_string, request, jsonify, session,render_template 
from utils.database import get_db
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
from sqlalchemy import text
from datetime import datetime

# Create a Blueprint
messages = Blueprint('messages', __name__)
def generate_conversation_id():
    """Generate a 15-digit conversation ID combining timestamp and random digits"""
    import random
    import time
    
    # Get current timestamp (last 6 digits)
    timestamp_part = str(int(time.time() * 1000))[-6:]
    
    # Generate random 9 digits
    random_part = ''.join([str(random.randint(0, 9)) for _ in range(9)])
    
    # Combine to make 15 digits
    return timestamp_part + random_part

@messages.route('/chat', methods=['GET'])
@verify_user
@is_email_verified
def chat():
    return render_template('/pages/messaging/message.html')


# Example: GET all messages for the current user
@messages.route('/messages', methods=['GET'])
@verify_user
@is_email_verified
def get_messages():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401
    db = get_db()
    query = text("""
        SELECT * FROM messages WHERE sender_id = :user_id OR receiver_id = :user_id ORDER BY sent_at DESC
    """)
    result = db.execute(query, {'user_id': user_id})
    messages_list = [dict(row) for row in result]
    return jsonify(messages_list)

# Example: POST a new message
@messages.route('/messages', methods=['POST'])
@verify_user
@is_email_verified
def send_message():
    sender_id = session.get('user_id')
    if not sender_id:
        return jsonify({'error': 'Not authenticated'}), 401
    data = request.get_json()
    receiver_id = data.get('receiver_id')
    message_content = data.get('message')
    if not receiver_id or not message_content:
        return jsonify({'error': 'Invalid message data'}), 400
    db = get_db()
    query = text("""
        INSERT INTO messages (sender_id, receiver_id, content, sent_at,conversation_id)
        VALUES (:sender_id, :receiver_id, :content, :sent_at, :conversation_id)
    """)
    result = db.execute_query(query, {
        'sender_id': sender_id,
        'receiver_id': receiver_id,
        'content': message_content,
        'sent_at': datetime.utcnow(),
        'conversation_id': generate_conversation_id()
    })
    print(result)
    if not result['success']:
        return jsonify({'error': 'Failed to send message'}), 500
    return jsonify({ 'status': 'sent'})

# Example: GET messages between two users
@messages.route('/messages/conversation/<string:conversation_id>', methods=['GET'])
@verify_user
@is_email_verified
def get_conversation(conversation_id):
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401
    db = get_db()
    query = text("""
        SELECT m.*, 
               CASE WHEN m.sender_id = :user_id THEN 'sent' ELSE 'received' END as message_type
        FROM messages m
        WHERE m.conversation_id = :conversation_id and (m.sender_id = :user_id OR m.receiver_id = :user_id)
        ORDER BY m.sent_at ASC
    """)
    result = db.execute_query(query, {'user_id': user_id, 'conversation_id': conversation_id})
    if result['output']:
        
        html_messages = []
        for message in result['output']:
            message_class = 'message sent mb-3 text-end' if message['message_type'] == 'sent' else 'message received mb-3'
            bubble_class = 'bubble d-inline-block p-3 rounded-4 bg-primary text-white' if message['message_type'] == 'sent' else 'bubble d-inline-block p-3 rounded-4 bg-light'
            time_class = 'small text-white-50 mt-1' if message['message_type'] == 'sent' else 'small text-muted mt-1'
            print("message:",message)
            sent_time = message['sent_at'].strftime('%d %b %Y %I:%M %p') if message['sent_at'] else ''
            
            html_messages.append(f"""
            <div class=\"{message_class}\">
                <div class=\"{bubble_class}\">
                    {message['content']}
                    <div class=\"{time_class}\">{sent_time}</div>
                </div>
            </div>
            """)
        return ''.join(html_messages)
    return "<div class='alert alert-info'>No messages found</div>"

@messages.route('/api/messages/history/<int:other_user_id>', methods=['GET'])
@verify_user
@is_email_verified
def get_message_history(other_user_id):
    user_id = session.get('user_id')
    db = get_db()
    
    query = text("""
        SELECT m.message_id, m.sender_id, m.content, m.sent_at,
               CASE WHEN m.sender_id = :user_id THEN 'sent' ELSE 'received' END as type
        FROM messages m
        WHERE (m.sender_id = :user_id AND m.receiver_id = :other_user_id)
           OR (m.sender_id = :other_user_id AND m.receiver_id = :user_id)
        ORDER BY m.sent_at DESC
        LIMIT 50
    """)
    
    result = db.execute_query(query, {
        'user_id': user_id,
        'other_user_id': other_user_id
    })
    
    if result['success']:
        messages = [{
            'message_id': msg['message_id'],
            'sender_id': msg['sender_id'],
            'content': msg['content'],
            'sent_at': msg['sent_at'].isoformat() if msg['sent_at'] else None,
            'type': msg['type']
        } for msg in result['output']]
        return jsonify({'success': True, 'messages': messages})
    return jsonify({'success': False, 'message': 'Failed to fetch messages'}), 500

@messages.route('/api/messages/users/search', methods=['GET'])
@verify_user
@is_email_verified
def search_users():
    search_term = request.args.get('q', '')
    user_id = session.get('user_id')
    db = get_db()
    
    query = text("""
        SELECT 
            js.seeker_id as user_id,
            js.email,
            'job_seeker' as user_type,
            CONCAT(js.first_name, ' ', js.last_name) as display_name,
            NULL as degree,
            NULL as school_graduated,
            NULL as certifications,
            NULL as specialized_training
        FROM job_seekers js
        WHERE LOWER(CONCAT(js.first_name, ' ', js.last_name)) LIKE :search_pattern
            OR LOWER(js.email) LIKE :search_pattern

        UNION ALL

        SELECT 
            e.employer_id as user_id,
            e.email,
            'employer' as user_type,
            e.company_name as display_name,
            NULL as degree,
            NULL as school_graduated,
            NULL as certifications,
            NULL as specialized_training
        FROM employers e
        WHERE LOWER(e.company_name) LIKE :search_pattern
            OR LOWER(e.email) LIKE :search_pattern
    """)
    
    result = db.execute_query(query, {
        'user_id': user_id,
        'search_pattern': f'%{search_term.lower()}%'
    })
    if not result['output']:
         return """
            <div class="card">
                <div class="card-body text-center">
                    <i class="bi bi-search text-muted fs-1"></i>
                    <h5 class="card-title mt-3">No Results Found</h5>
                    <p class="card-text">We couldn't find any users matching your search.</p>
                    <p class="text-muted">Try different search terms</p>
                </div>
            </div>
            """
    if result['success']:
    
        html_items = []
        for user in result['output']:
        
            html_items.append(f"""
                <li class="list-group-item d-flex align-items-center p-3" onclick="window.location.href='/messages/{user['user_id']}'">
                    <img src="https://api.dicebear.com/7.x/initials/svg?seed={user['display_name'][0]}" height="50" class="rounded-circle me-3" alt="Avatar">
                    <div class="flex-grow-1">
                        <div class="fw-bold">{user['display_name']}</div>
                        <small class="text-muted">{user['email']}</small>
                    </div>
                    <small class="text-muted">{user['user_type']}</small>
                </li>
            """)
        return ''.join(html_items)
       
   
    return """
    <div class="card">
        <div class="card-body text-center">
            <i class="bi bi-exclamation-triangle-fill text-danger fs-1"></i>
            <h5 class="card-title mt-3">Search Failed</h5>
            <p class="card-text">We couldn't complete your search. Please try again later.</p>
            <button class="btn btn-primary" onclick="retrySearch()">Try Again</button>
        </div>
    </div>
    """



