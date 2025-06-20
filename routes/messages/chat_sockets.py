from asyncio import BrokenBarrierError
from datetime import datetime

from flask import (
    Blueprint,
    jsonify,
    render_template,
    render_template_string,
    request,
    session,
)
from flask_socketio import SocketIO, emit
from sqlalchemy import text

from middlewares.is_email_verified import is_email_verified
from middlewares.verify_user import verify_user
from utils.check_if_exists import check_column_exists
from utils.database import get_db

socketio = SocketIO()

clients = {}


def get_conversation_by_receiver(user1_id, user2_id):
    db = get_db()
    query = text("""
        SELECT conversation_id 
        FROM messages 
        WHERE (sender_id = :user1_id AND receiver_id = :user2_id)
           OR (sender_id = :user2_id AND receiver_id = :user1_id)
        ORDER BY sent_at DESC
        LIMIT 1
    """)
    result = db.execute_query(query, {"user1_id": user1_id, "user2_id": user2_id})
    return result['output'][0]['conversation_id'] if result['success'] and result['output'] else None

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

def generate_conversation_id():
    import random
    import time
    timestamp_part = str(int(time.time() * 1000))[-6:]
    random_part = ''.join([str(random.randint(0, 9)) for _ in range(9)])
    return timestamp_part + random_part

def get_user_type_and_info(user_id):
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




def init_socketio(app):
    socketio.init_app(app)
    return socketio



@socketio.on('location')
def handle_location(data):
    print(data,"*"*100000)
    logging.debug(f"Received location data: {data}")
    emit('update', data, broadcast=True)

@socketio.on('send_message')
def handle_send_message(message_content, receiver_id, conversation_id):
    sender_id = session.get('user_id')
    if session.get('user_type') == 'seeker':
        sender_type ='job_seeker'
    else:
        sender_type ='employer'
    if not receiver_id or not message_content:
       
        return emit('error', {'message': 'Invalid message data'})
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
        return emit('error', {'message': 'Failed to send message'})
    emit('receive_message', {'message': message_content, 'receiver_id': receiver_id, 'sender_id': sender_id, 'conversation_id': conversation_id}, broadcast=True)
    # return jsonify({ 'status': 'sent'})


@socketio.on('get_conversations')
def handle_get_conversations(data):
    user_id = session.get('user_id')
    receiver_id = data['receiver_id']
    if user_id == receiver_id:
        print(f'event triggered ===getting conversations=== user_id: {user_id} receiver_id: {receiver_id}')
        print(f"getting the latest conversation of {data['sender_id']}")

@socketio.on('receive_message')
def handle_receive_message(data):
    user_id = session.get('user_id')
    print(f"event triggered ===received message=== user_id: {user_id} receiver_id: {data['receiver_id']}")
    print(data)
    if user_id == data['receiver_id']:
        print('hey fucker you have a new message!!')
        socketio.emit('receive_message', data)
    

@socketio.on('disconnect')
def handle_disconnect():
    client_id = request.sid
    print(f'Client disconnected: {client_id}')
    if client_id in clients:
        del clients[client_id]
    print(f'Client disconnected: {client_id}')


@socketio.on('connect')
def handle_connect():
    client_id = request.sid
    user_id = session.get('user_id')
    clients[user_id] = {'id': client_id}
    print(f'Client connected: {client_id}')
    print("connected clients: ", clients)
    # email = session.get('email')
    # print(email)
    # print('connected')
    # socketio.emit('user_connected', {'email': email})

@socketio.on('get_conversation_list')
def handle_get_conversation_list():
    print('event triggered === gettign conversations === user_id: {session.get("user_id")}')
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
    <li class=\"list-group-item d-flex align-items-center p-3 id-{partner_id}" id="{partner_id}" data-cl-id="{partner_id}" onclick=\"window.location.href='/messages/{partner_id}'\">  <img src=\"https://api.dicebear.com/7.x/initials/svg?seed={display_name[0] if display_name else ''}\" height=\"50\" class=\"rounded-circle me-3\" alt=\"Avatar\">
                    <div id="{partner_id}" class=\"flex-grow-1\">
                        <div id="{partner_id}" class=\"fw-bold\">{display_name}</div>
                        <small id="{partner_id}"  class=\"text-muted\">{email}</small>
                    </div>
                    <small id="{partner_id}" class=\"text-muted\">{user_type_str}</small>
                    
                </li>
            """)
        data = ''.join(html_items)
        return emit('refresh_convo_list', {'data': data})
        
    data =  "<div class='alert alert-info'>No chat partners found</div>"
    emit('refresh_convo_list', {'data': data})
    return 

@socketio.on('get_conversation')
def get_conversation(conversation_id):
    user_id = session.get('user_id')
    print('event triggered === getting conversation === conversation id:',conversation_id)
    if not conversation_id:
        return emit('refresh_conversation', {'data' : """
            <div class=\"alert alert-warning text-center\">
                <i class=\"bi bi-chat-dots fs-1\"></i>
                <h5 class=\"mt-3\">No Conversation Selected</h5>
                <p>Please select a conversation to view messages.</p>
            </div>
        """})
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
            message['content'] = message['content'].replace('&', '&amp;')\
                .replace('<', '&lt;')\
                .replace('>', '&gt;')\
                .replace('"', '&quot;')\
                .replace("'", '&#039;')
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
        return emit('refresh_conversation', {'data': ''.join(html_messages)})
    return emit('refresh_conversation', {'data': "<div class='alert alert-info'>No messages found</div>"})
    
@socketio.on('get_online_users')
def get_online_users():
    db = get_db()
    user_id = session.get('user_id')
    query = text("""
        SELECT sender_id, receiver_id from messages
        WHERE sender_id  = :user_id or receiver_id = :user_id
    """)
    result = db.execute_query(query, {'user_id': user_id})
    output = result['output']
    collected_ids = []
    for id in output:
        if not id['sender_id'] == user_id:
           collected_ids.append(id['sender_id'])
    online = [users for users in clients if users in collected_ids]
    print('online users: ', online)
    return emit('refresh_online_users', {'data': online})