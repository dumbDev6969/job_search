from datetime import datetime

from flask import *
from sqlalchemy import text

from middlewares.is_email_verified import is_email_verified
from middlewares.verify_user import verify_user
from utils.check_if_exists import check_column_exists
from utils.database import get_db
conversation_route = Blueprint('conversation_route', __name__)



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


@conversation_route.route('/messages/delete-conversation', methods=['POST'])
@verify_user
@is_email_verified
def delete_conversation_route():
    db = get_db()
    conversation_id = request.form.get('conversation_id')
    is_deleted = check_column_exists('deleted_messages', 'conversatio_id ', conversation_id)
    if is_deleted:
        return jsonify(success=False, message='Conversation already deleted'), 400
    sender_id = session.get('user_id')
    print(f"Deleting conversation with ID: {conversation_id} user id: {sender_id}", request.form)
    if not conversation_id:
        return jsonify(success=False, error='Invalid request'), 400
    
    query = text("""
        INSERT INTO deleted_messages (conversatio_id, sender_id)
        VALUES (:conversation_id, :sender_id)
    """)
    result = db.execute_query(query, {"conversation_id": conversation_id, "sender_id": sender_id})
    if result['success']:
        return jsonify(success=True, message='Conversation deleted successfully'), 200
    else:
        return jsonify(success=False, error='Failed to delete conversation'), 500

@conversation_route.route('/messages/<int:user_id>/<string:coversation_id>', methods=['GET'])
@conversation_route.route('/messages/<int:user_id>', methods=['GET'])
@verify_user
@is_email_verified
def get_conversation_route(user_id=None, coversation_id=None):
    db = get_db()
    user_type, info, name, email = get_user_type_and_info(user_id)
    if not info:
        return render_template('/pages/user_not_found.html'), 404
    if user_id and not coversation_id:
        coversation_id = get_conversation_by_receiver(user_id, session['user_id']) or generate_conversation_id()
        return redirect(f'/messages/{user_id}/{coversation_id}')
    query = text("SELECT * FROM messages WHERE conversation_id = :conversation_id ORDER BY sent_at ASC")
    result = db.execute_query(query, {"conversation_id": coversation_id})
    if result['success'] and result['output']:
        # Optionally process messages if needed
        pass
    sender = get_user_type_and_info(session.get('user_id'))
    if sender[0] == 'employer':
        sender_name = sender[1]['company_name']
    else:
        sender_name = sender[1]['first_name'] + ' ' + sender[1]['last_name']
    sender_type = sender[0]
    sender_id = session.get('user_id')


    if user_type == 'employer':
        return render_template('/pages/messaging/message.html', coversation_id=coversation_id, info=info, name=name, email=email, user_id=user_id, user_type=user_type, sender_name=sender_name, sender_type=sender_type, sender_id=sender_id,is_job_seeker=True)
    elif user_type == 'jobseeker':
        return render_template('/pages/messaging/message.html', coversation_id=coversation_id, info=info, name=name, email=email, user_id=user_id, user_type=user_type, sender_name=sender_name, sender_type=sender_type, sender_id=sender_id, is_job_seeker=False)
    return redirect('messages')

@conversation_route.route('/api/messages/chat-partners', methods=['GET'])
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
                <li class=\"list-group-item d-flex align-items-center p-3\" id=\"{partner_id}\" data-cl-id=\"{partner_id}\" onclick=\"window.location.href='/messages/{partner_id}'\">
                    <img  id=\"{partner_id}\" src=\"https://api.dicebear.com/7.x/initials/svg?seed={display_name[0] if display_name else ''}\" height=\"50\" class=\"rounded-circle me-3\" alt=\"Avatar\">
                    <div id=\"{partner_id}\" class=\"flex-grow-1\">
                        <div id=\"{partner_id}\" class=\"fw-bold\">{display_name}</div>
                        <small id=\"{partner_id}\" class=\"text-muted\">{email}</small>
                    </div>
                    <small id=\"{partner_id}\" class=\"text-muted\">{user_type_str}</small>
                </li>
            """)
        return ''.join(html_items)
    return "<div class='alert alert-info'>No chat partners found</div>"
