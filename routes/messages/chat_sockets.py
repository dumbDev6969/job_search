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
    """
    Retrieves the most recent conversation ID between two users.

    Args:
        user1_id (int): The ID of the first user.
        user2_id (int): The ID of the second user.

    Returns:
        int or None: The ID of the conversation if found; otherwise, None.
    """

    db = get_db()
    logging.info(f"Fetching conversation between user {user1_id} and user {user2_id}")
    query = text("""
        SELECT conversation_id 
        FROM messages 
        WHERE (sender_id = :user1_id AND receiver_id = :user2_id)
           OR (sender_id = :user2_id AND receiver_id = :user1_id)
        ORDER BY sent_at DESC
        LIMIT 1
    """)
    result = db.execute_query(query, {"user1_id": user1_id, "user2_id": user2_id})
    
    if result['success']:
        if result['output']:
            conversation_id = result['output'][0]['conversation_id']
            logging.info(f"Found conversation ID: {conversation_id}")
            return conversation_id
        else:
            logging.warning("No conversation found")
            return None
    else:
        logging.error("Failed to execute query")
        return None

def get_user_info(user_id, user_type):
    """
    Fetches user information given user ID and type.

    Args:
        user_id (int): The ID of the user.
        user_type (str): The type of the user, either 'jobseeker' or 'employer'.

    Returns:
        dict: The user information, or None if the user type is not supported or
            the query fails.
    """
    logging.info(f"Fetching user info for user ID: {user_id}, type: {user_type}")
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
        logging.warning(f"User type '{user_type}' is not supported")
        return None
    result = db.execute_query(query, {"user_id": user_id})
    if result['success'] and result['output']:
        logging.info(f"User info fetched successfully for user ID: {user_id}")
        return result['output'][0]
    else:
        logging.error(f"Failed to fetch user info for user ID: {user_id}")
        return None

def generate_conversation_id():
    """
    Generates a unique conversation ID using a combination of the current timestamp
    and a random number. The timestamp part is derived from the current time in 
    milliseconds, taking the last 6 digits, and the random part is a 9-digit number 
    generated randomly. The function logs the generated parts for debugging purposes.
    
    Returns:
        str: A unique conversation ID.
    """

    import random
    import time
    timestamp_part = str(int(time.time() * 1000))[-6:]
    logging.info(f"Generated timestamp part: {timestamp_part}")
    random_part = ''.join([str(random.randint(0, 9)) for _ in range(9)])
    logging.info(f"Generated random part: {random_part}")
    return timestamp_part + random_part

def get_user_type_and_info(user_id):
    """
    Determines the type and information of a user based on their user ID.

    This function checks if the given user ID belongs to a job seeker or an employer
    by verifying their presence in respective database tables. It then retrieves
    relevant user information based on the user type.

    Args:
        user_id (int): The ID of the user to be checked.

    Returns:
        tuple: A tuple containing the user type ('jobseeker' or 'employer'), a
        dictionary of user information, the user's name, and email. Returns 
        (None, None, '', '') if the user ID does not correspond to a valid user.
    """

    logging.info(f"Checking user type and info for user ID: {user_id}")
    is_seeker = check_column_exists('job_seekers', 'seeker_id ', user_id)
    is_employer = check_column_exists('employers', 'employer_id ', user_id)
    if is_seeker:
        logging.info(f"User {user_id} is a job seeker")
        info = get_user_info(user_id, 'jobseeker')
        name = info['first_name'] + ' ' + info['last_name'] if info else ''
        email = info['email'] if info else ''
        return 'jobseeker', info, name, email
    elif is_employer:
        logging.info(f"User {user_id} is an employer")
        info = get_user_info(user_id, 'employer')
        name = info['company_name'] if info else ''
        email = info['email'] if info else ''
        return 'employer', info, name, email
    logging.warning(f"User ID {user_id} does not correspond to a valid user")
    return None, None, '', ''




def init_socketio(app):
    """
    Initializes the Socket.IO server with the given Flask application.

    This function configures the Socket.IO server to work with the provided
    Flask app instance, enabling real-time bidirectional communication
    capabilities.

    Args:
        app (Flask): The Flask application instance to integrate with Socket.IO.

    Returns:
        SocketIO: The initialized Socket.IO server instance.
    """

    socketio.init_app(app)
    return socketio



@socketio.on('location')
def handle_location(data):
    """
    Handles the 'location' event from a client and broadcasts the location data to all connected clients.

    This function listens for the 'location' event emitted by clients, logs the received location data for
    debugging purposes, and then broadcasts the data to all connected clients using the 'update' event.

    Args:
        data (dict): A dictionary containing location data sent by the client.
    """

    print(data,"*"*100000)
    logging.debug(f"Received location data: {data}")
    emit('update', data, broadcast=True)

@socketio.on('send_message')
def handle_send_message(message_content, receiver_id, conversation_id):
    """
    Handles the 'send_message' event from a client and processes the message content.

    This function listens for the 'send_message' event emitted by clients, extracts the message content,
    receiver ID, and conversation ID from the event data, and inserts the message into the database.
    If the message data is invalid or the database operation fails, it emits an error event.
    Otherwise, it broadcasts the message to all connected clients using the 'receive_message' event.

    Args:
        message_content (str): The content of the message being sent.
        receiver_id (int): The ID of the user receiving the message.
        conversation_id (str): The ID of the conversation the message belongs to.
    """
    
    sender_id = session.get('user_id')
    if not sender_id:
        logging.error(f"User not authenticated for message from {request.sid}")
        return emit('error', {'message': 'Not authenticated'})

    sender_type = 'job_seeker' if session.get('user_type') == 'seeker' else 'employer'
    
    if not receiver_id or not message_content:
        logging.warning(f"Invalid message data from {request.sid} for conversation {conversation_id}: missing receiver_id or message_content")
        return emit('error', {'message': 'Invalid message data'})

    db = get_db()
    query = text("""
        INSERT INTO messages (sender_id, receiver_id, content, sent_at, conversation_id, sender_type)
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
        logging.error(f"Failed to insert message into database from {request.sid} for conversation {conversation_id}")
        return emit('error', {'message': 'Failed to send message'})

    logging.info(f"Message sent successfully from user {sender_id} to user {receiver_id} in conversation {conversation_id} via {request.sid}")
    emit('receive_message', {'message': message_content, 'receiver_id': receiver_id, 'sender_id': sender_id, 'conversation_id': conversation_id}, broadcast=True)


@socketio.on('get_conversations')
def handle_get_conversations(data):
    """
    Handles the 'get_conversations' event to retrieve conversations for the current user.

    This function listens for the 'get_conversations' event emitted by clients, retrieves the
    current user's ID from the session, and checks if the user is the intended receiver. If so,
    it logs the event details and initiates the process to get the latest conversation for the
    specified sender.

    Args:
        data (dict): A dictionary containing the receiver ID and sender ID information.
    """

    user_id = session.get('user_id')
    receiver_id = data.get('receiver_id')

    if user_id == receiver_id:
        logging.info(f"Event triggered: 'get_conversations' for user_id: {user_id}, receiver_id: {receiver_id}")
        logging.info(f"Retrieving the latest conversation for sender_id: {data.get('sender_id')}")
    else:
        logging.warning(f"User ID mismatch: session user_id: {user_id}, data receiver_id: {receiver_id}")

@socketio.on('receive_message')
def handle_receive_message(data):
    """
    Handles the 'receive_message' event to receive a new message from another user.

    This function listens for the 'receive_message' event emitted by clients, retrieves the
    current user's ID from the session, and checks if the user is the intended receiver. If so,
    it logs the event details and broadcasts the message to the specified receiver.

    Args:
        data (dict): A dictionary containing the message content, sender ID, and receiver ID.
    """
    user_id = session.get('user_id')
    logging.info(f"Event 'receive_message' triggered for user_id: {user_id}, receiver_id: {data['receiver_id']}")
    logging.debug(f"Received data: {data}")
    
    if user_id == data['receiver_id']:
        logging.info(f"User {user_id} is the intended receiver. Broadcasting message.")
        socketio.emit('receive_message', data)
    else:
        logging.warning(f"User ID mismatch: session user_id: {user_id}, data receiver_id: {data['receiver_id']}")
    

@socketio.on('disconnect')
def handle_disconnect():
    """
    Handles the 'disconnect' event for a client.

    This function is triggered when a client disconnects from the socket.
    It logs the client ID and removes the client from the 'clients' dictionary
    if it exists, effectively managing the client's disconnection.
    """

    client_id = request.sid
    logging.info(f'Client attempting to disconnect: {client_id}')
    
    if client_id in clients:
        del clients[client_id]
        logging.info(f'Client successfully disconnected: {client_id}')
    else:
        logging.warning(f'Tried to disconnect non-existent client: {client_id}')


@socketio.on('connect')
def handle_connect():
    """
    Handles the 'connect' event for a client.

    This function is triggered when a client connects to the socket. It retrieves the client's
    session ID and user ID, stores the client information in the 'clients' dictionary, and logs
    the connection details. Optionally, it can emit the 'user_connected' event with the user's
    email.

    Side Effects:
        - Updates the global 'clients' dictionary with the connected client's information.
        - Logs connection details to the console.
    """

    client_id = request.sid
    user_id = session.get('user_id')
    clients[user_id] = {'id': client_id}
    logging.info(f'Client connected: {client_id} (User ID: {user_id})')
    logging.info(f'Connected clients: {clients}')
    # email = session.get('email')
    # logging.info(f'User email: {email}')
    # socketio.emit('user_connected', {'email': email})

@socketio.on('get_conversation_list')
def handle_get_conversation_list():
    """
    Handles the 'get_conversation_list' event to retrieve and emit the list of conversation partners.

    This function listens for the 'get_conversation_list' event emitted by clients, retrieves the 
    current user's ID from the session, and queries the database to find distinct conversation partners 
    for the user. It constructs an HTML list of these partners and emits the 'refresh_convo_list' event 
    with the generated HTML content. If no partners are found, it emits an alert message indicating no 
    chat partners.

    Side Effects:
        - Emits 'refresh_convo_list' event with HTML data of conversation partners or an alert message.
    """

    logging.info(f'Event triggered: get_conversation_list for user_id: {session.get("user_id")}')
    user_id = session.get('user_id')
    db = get_db()
    query = text("""
        SELECT DISTINCT 
            CASE 
                WHEN sender_id = :user_id THEN receiver_id 
                ELSE sender_id 
            END as partner_id,
                 conversation_id
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

            sql = text("SELECT * FROM deleted_messages WHERE conversatio_id = :conversation_id AND sender_id = :user_id")
            result = db.execute_query(sql, {'conversation_id': partner['conversation_id'], 'user_id': user_id})

          
            if not result['output']:
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
        logging.info(f'Found partners for user_id: {user_id}')
        return emit('refresh_convo_list', {'data': data})
        
    logging.warning(f'No partners found for user_id: {user_id}')
    data =  "<div class='alert alert-info'>No chat partners found</div>"
    emit('refresh_convo_list', {'data': data})
    return 

@socketio.on('get_conversation')
def get_conversation(conversation_id):
    """
    Handles the 'get_conversation' event to retrieve and emit the list of messages in a conversation.

    This function listens for the 'get_conversation' event emitted by clients, retrieves the current user's ID from the session, and queries the database to find the messages in the specified conversation. It constructs an HTML list of these messages and emits the 'refresh_conversation' event with the generated HTML content. If no messages are found, it emits an alert message indicating no messages found.

    Side Effects:
        - Emits 'refresh_conversation' event with HTML data of conversation messages or an alert message.
    """

    user_id = session.get('user_id')
    logging.info(f'Event triggered: get_conversation for user_id: {user_id}, conversation_id: {conversation_id}')
    if not conversation_id:
        logging.warning(f'No conversation ID provided. Emitting alert message.')
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
        logging.info(f'Found messages for conversation_id: {conversation_id}')
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
            sql = text("SELECT * FROM deleted_messages WHERE conversatio_id = :conversation_id AND sender_id = :user_id")
            result = db.execute_query(sql, {'conversation_id':conversation_id, 'user_id': user_id})
            if not result['output']:
                html_messages.append(f"""
                    <div class=\"{message_class}\">
                        <div class=\"{bubble_class}\">
                            {message['content']}
                            <div class=\"{time_class}\">{sent_time}</div>
                        </div>
                    </div>
                """)
            else:
                 return emit('refresh_conversation', {'data' : """
            <div class=\"alert alert-warning text-center\">
                <i class=\"bi bi-chat-dots fs-1\"></i>
                <h5 class=\"mt-3\">No Conversation Selected</h5>
                <p>Please select a conversation to view messages.</p>
            </div>
        """})
        return emit('refresh_conversation', {'data': ''.join(html_messages)})
    logging.warning(f'No messages found for conversation_id: {conversation_id}')
    return emit('refresh_conversation', {'data': "<div class='alert alert-info'>No messages found</div>"})
    
@socketio.on('get_online_users')
def get_online_users():
    """
    Handles the 'get_online_users' event to retrieve and emit the list of online users
    with whom the current user has a conversation.

    This function listens for the 'get_online_users' event emitted by clients, retrieves the
    current user's ID from the session, and queries the database to find distinct
    conversation partners for the user. It constructs a list of these partners and emits the
    'refresh_online_users' event with the generated list content. If no partners are found, it
    emits an alert message indicating no online users.

    Side Effects:
        - Emits 'refresh_online_users' event with list data of online users or an alert message.
    """

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