from flask import *
from utils.database import get_db
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
from sqlalchemy import text
from datetime import datetime
from utils.check_if_exists import check_column_exists
conversation_route = Blueprint('conversation_route', __name__)


def get_conversation_by_receiver(receiver_id):
    """Get conversation ID using receiver_id"""
    db = get_db()
    query = text("""
        SELECT conversation_id 
        FROM messages 
        WHERE receiver_id = :receiver_id
        ORDER BY sent_at DESC
        LIMIT 1
    """)
    result = db.execute_query(query, {"receiver_id": receiver_id})
    return result['output'][0]['conversation_id'] if result['success'] and result['output'] else None


def get_user_info(user_id, user_type):
    """Extract jobseeker or employer information by ID"""
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
    """Generate a 15-digit conversation ID combining timestamp and random digits"""
    import random
    import time
    
    # Get current timestamp (last 6 digits)
    timestamp_part = str(int(time.time() * 1000))[-6:]
    
    # Generate random 9 digits
    random_part = ''.join([str(random.randint(0, 9)) for _ in range(9)])
    
    # Combine to make 15 digits
    return timestamp_part + random_part



@conversation_route.route('/messages/<int:user_id>/<string:coversation_id>', methods=['GET'])
@conversation_route.route('/messages/<int:user_id>', methods=['GET'])
@verify_user
@is_email_verified
def get_conversation_route(user_id=None, coversation_id=None):
    db = get_db()
    if check_column_exists('messages', 'receiver_id ', user_id):
        coversation_id = get_conversation_by_receiver(user_id)
        em = check_column_exists('employers', 'employer_id ', user_id)   
        js = check_column_exists('job_seekers', 'seeker_id ', user_id)   
        jobseeker_info = get_user_info(user_id, 'jobseeker')
        employer_info = get_user_info(user_id, 'employer')
        if em:
            name = employer_info['company_name']
            email = employer_info['email']
        
            return render_template('/pages/messaging/message.html', coversation_id=coversation_id,info=employer_info, name=name, email=email,user_id=user_id)
        elif js:
            name = jobseeker_info['first_name'] + ' ' + jobseeker_info['last_name']
            email = jobseeker_info['email']
            return render_template('/pages/messaging/message.html', coversation_id=coversation_id,info=jobseeker_info, name=name, email=email, user_id=user_id)

    if user_id:
        if not coversation_id:
          
            conversation_id = generate_conversation_id()
            redirect(f'/messages/{user_id}/{conversation_id}')

    query = text("SELECT * FROM messages WHERE conversation_id = :conversation_id ORDER BY sent_at ASC")
    result = db.execute_query(query, {"conversation_id": coversation_id})
   
    if result['success']:
        if result['output']:
            for row in result['output']:

                conversation_id = row['conversation_id']
                sender_id = row['sender_id']
                receiver_id = row['receiver_id']
                sender_type = row['sender_type']
                content = row['content']
                sent_at = row['sent_at']
                is_read = row['is_read']
                print("conversation_id:", conversation_id)

                jobseeker_info = get_user_info(session['user_id'], 'jobseeker')
                employer_info = get_user_info(receiver_id, 'employer')
            
            return render_template('/pages/messaging/message.html', coversation_id=conversation_id)
    em = check_column_exists('employers', 'employer_id ', user_id)   
    js = check_column_exists('job_seekers', 'seeker_id ', user_id)   
    jobseeker_info = get_user_info(user_id, 'jobseeker')
    employer_info = get_user_info(user_id, 'employer')
    if em:
        name = employer_info['company_name']
        email = employer_info['email']
     
        return render_template('/pages/messaging/message.html', coversation_id=coversation_id,info=employer_info, name=name, email=email,user_id=user_id)
    elif js:
        name = jobseeker_info['first_name'] + ' ' + jobseeker_info['last_name']
        email = jobseeker_info['email']
        return render_template('/pages/messaging/message.html', coversation_id=coversation_id,info=jobseeker_info, name=name, email=email, user_id=user_id)
    return redirect('/chat')





@conversation_route.route('/api/messages/chat-partners/<int:coversation_id>', methods=['GET'])
@verify_user
@is_email_verified
def get_chat_partners(coversation_id):
    user_id = session.get('user_id')
  
  
    db = get_db()
    query = text("""
        SELECT DISTINCT 
            CASE WHEN sender_id = :user_id THEN receiver_id ELSE sender_id END as partner_id,
            CASE WHEN sender_id = :user_id THEN 'sent' ELSE 'received' END as direction
        FROM messages
        WHERE sender_id = :user_id
        ORDER BY direction DESC
    """)
    
    result = db.execute_query(query, {'user_id': user_id, 'coversation_id': coversation_id})
    
    print("HOSYOTRYYY",result)
    if result['output']:
        partners =result['output']
        print('partner length:',len(partners))
     
        html_items = []
        for partner in partners:
            
            partner_id = partner['partner_id']
            print("partner:",partner)
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
                WHERE js.seeker_id = :user_id 

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
                WHERE e.employer_id = :user_id
            """)
        
            users = db.execute_query(query, {
                'user_id': partner_id,
            })
            
            print('users:::::::',users)
           

            for user in users['output']:
                html_items.append(f"""
                    <li class="list-group-item d-flex align-items-center p-3" onclick="window.location.href = '/messages/{user['user_id']}';">
                            <img src="https://api.dicebear.com/7.x/initials/svg?seed={user['display_name'][0]}" height="50" class="rounded-circle me-3" alt="Avatar">
                            <div class="flex-grow-1">
                                <div class="fw-bold">{user['display_name']}</div>
                                <small class="text-muted">{user['email']}</small>
                            </div>
                            <small class="text-muted">{user['user_type']}</small>
                        </li>
                    """
                )
              
            
        return ''.join(html_items)
    return """
    <li class="list-group-item d-flex align-items-center p-3">
                  <img src="/assets/img/default_profile.jpg" height="50"class="rounded-circle me-3" alt="Avatar">
                  <div class="flex-grow-1">
                    <div class="fw-bold">TechCorp</div>
                    <small class="text-muted">...</small>
                  </div>
                  <small class="text-muted">1 Dec 2020</small>
                </li>
                
                <!-- Active Chat Item -->
                <li class="list-group-item d-flex align-items-center p-3 bg-dark-subtle">
                  <img src="/assets/img/default_profile.jpg" height="50" class="rounded-circle me-3" alt="Avatar">
                  <div class="flex-grow-1">
                    <div class="fw-bold">TechSprint</div>
                    <small class="text-muted">Lorem, ipsum dolor.</small>
                  </div>
                  <small class="text-muted">17 Sept 2020</small>
                </li>
    """






