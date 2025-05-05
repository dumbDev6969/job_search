from datetime import datetime

from flask import (
    Blueprint,
    jsonify,
    render_template,
    render_template_string,
    request,
    session,
)
from sqlalchemy import text

from middlewares.is_email_verified import is_email_verified
from middlewares.verify_user import verify_user
from utils.database import get_db

def generate_conversation_id():
    import random
    import time
    timestamp_part = str(int(time.time() * 1000))[-6:]
    random_part = ''.join([str(random.randint(0, 9)) for _ in range(9)])
    return timestamp_part + random_part

def get_user_info(user_id, user_type):
    db = get_db()
    if user_type == 'jobseeker':
        query = text("""
            SELECT q.*, js.* 
            FROM qualifications q
            JOIN job_seekers js ON q.seeker_id = js.seeker_id
            WHERE q.seeker_id = :user_id
        """)
    elif user_type == 'employer':
        query = text("""
            SELECT * FROM employers
            WHERE employer_id = :user_id
        """)
    else:
        return None
    result = db.execute_query(query, {"user_id": user_id})
    return result['output'][0] if result['success'] and result['output'] else None

def get_user_type_and_info(user_id):
    from utils.check_if_exists import check_column_exists
    is_seeker = check_column_exists('job_seekers', 'seeker_id ', user_id)
    is_employer = check_column_exists('employers', 'employer_id ', user_id)
    if is_seeker:
        info = get_user_info(user_id, 'jobseeker')
        name = info['first_name'] + ' ' + info['last_name'] if info else ''
        email = info['email'] if info else ''
        return 'jobseeker', info, name, email
    elif is_employer:
        info = get_user_info(user_id, 'employer')
        name = info['company_name'] if info else ''
        email = info['email'] if info else ''
        return 'employer', info, name, email
    return None, None, '', ''

messages = Blueprint('messages', __name__)

@messages.route('/messages', methods=['GET'])
@verify_user
@is_email_verified
def get_messages():
    sender = get_user_type_and_info(session.get('user_id'))
    if sender[0] == 'employer':
        sender_name = sender[1]['company_name']
    else:
        sender_name = sender[1]['first_name'] + ' ' + sender[1]['last_name']
    sender_type = sender[0]
    sender_id = session.get('user_id')
    return render_template('/pages/messaging/message.html',  sender_name=sender_name, sender_type=sender_type, sender_id=sender_id)


@messages.route('/smessages', methods=['GET'])
def socket_mesasges():
    return render_template('/pages/messaging/socket_chats.html')

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
    conversation_id = data.get('conversation_id')

    if session.get('user_type') == 'seeker':
        sender_type ='job_seeker'
    else:
        sender_type ='employer'
    if not receiver_id or not message_content:
        return jsonify({'error': 'Invalid message data'}), 400
    db = get_db()
    query = text("""
        INSERT INTO messages (sender_id, receiver_id, content, sent_at,conversation_id, sender_type)
        VALUES (:sender_id, :receiver_id, :content, :sent_at, :conversation_id, :sender_type)
    """)
    result = db.execute_query(query, {
        'sender_id': sender_id,
        'receiver_id': receiver_id,
        'content': message_content,
        'sent_at': datetime.utcnow(),
        'conversation_id': conversation_id,
        'sender_type': sender_type
    })
    if not result['success']:
        return jsonify({'error': 'Failed to send message'}), 500
    return jsonify({ 'status': 'sent'})

@messages.route('/messages/conversation/<string:conversation_id>', methods=['GET'])
@messages.route('/messages/conversation/', methods=['GET'])
@verify_user
@is_email_verified
def get_conversation(conversation_id=None):
    user_id = session.get('user_id')
    if conversation_id is None:
        return """
            <div class=\"alert alert-warning text-center\">
                <i class=\"bi bi-chat-dots fs-1\"></i>
                <h5 class=\"mt-3\">No Conversation Selected</h5>
                <p>Please select a conversation to view messages.</p>
            </div>
        """
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
            <div class=\"card\">
                <div class=\"card-body text-center\">
                    <i class=\"bi bi-search text-muted fs-1\"></i>
                    <h5 class=\"card-title mt-3\">No Results Found</h5>
                    <p class=\"card-text\">We couldn't find any users matching your search.</p>
                    <p class=\"text-muted\">Try different search terms</p>
                </div>
            </div>
            """
    if result['success']:
        html_items = []
        for user in result['output']:
            html_items.append(f"""
                <li class=\"list-group-item d-flex align-items-center p-3\" onclick=\"window.location.href='/messages/{user['user_id']}'\">
                    <img src=\"https://api.dicebear.com/7.x/initials/svg?seed={user['display_name'][0]}\" height=\"50\" class=\"rounded-circle me-3\" alt=\"Avatar\">
                    <div class=\"flex-grow-1\">
                        <div class=\"fw-bold\">{user['display_name']}</div>
                        <small class=\"text-muted\">{user['email']}</small>
                    </div>
                    <small class=\"text-muted\">{user['user_type']}</small>
                </li>
            """)
        return ''.join(html_items)
    return "<div class='alert alert-info'>No users found</div>"

@messages.route('/api/messages/chat-partners', methods=['GET'])
@verify_user
@is_email_verified
def get_chat_partners():
    user_id = session.get('user_id')
    db = get_db()
    query = text("""
        SELECT DISTINCT 
            CASE 
                WHEN sender_id = :user_id THEN receiver_id 
                ELSE sender_id 
            END as partner_id
        FROM messages
        WHERE sender_id = :user_id OR receiver_id = :user_id
    """)
    result = db.execute_query(query, {'user_id': user_id})
    if result['output']:
        partners = result['output']
        html_items = []
        for partner in partners:
            partner_id = partner['partner_id']
            user_type, info, name, email = get_user_type_and_info(partner_id)
            display_name = name
            user_type_str = 'job_seeker' if user_type == 'jobseeker' else 'employer'
            html_items.append(f"""
                <li class=\"list-group-item d-flex align-items-center p-3\" onclick=\"window.location.href='/messages/{partner_id}'\">
                    <img src=\"https://api.dicebear.com/7.x/initials/svg?seed={display_name[0] if display_name else ''}\" height=\"50\" class=\"rounded-circle me-3\" alt=\"Avatar\">
                    <div class=\"flex-grow-1\">
                        <div class=\"fw-bold\">{display_name}</div>
                        <small class=\"text-muted\">{email}</small>
                    </div>
                    <small class=\"text-muted\">{user_type_str}</small>
                </li>
            """)
        return ''.join(html_items)
    return "<div class='alert alert-info'>No chat partners found</div>"



