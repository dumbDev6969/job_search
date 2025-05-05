import mysql.connector

class MessagingSystem:
    def __init__(self, db_config):
        """Initialize database connection"""
        self.db = mysql.connector.connect(**db_config)
    
    def _generate_conversation_id(self, sender_id, sender_type, receiver_id, receiver_type):
        """Generate a unique conversation ID based on participants"""
        participants = sorted([
            (sender_type.lower(), int(sender_id)),
            (receiver_type.lower(), int(receiver_id))
        ])
        return f"{participants[0][0]}_{participants[0][1]}_{participants[1][0]}_{participants[1][1]}"
    
    def send_message(self, sender_id, sender_type, receiver_id, receiver_type, content):
        """Send a new message between users"""
        conversation_id = self._generate_conversation_id(sender_id, sender_type, receiver_id, receiver_type)
        
        query = """
        INSERT INTO messages 
        (sender_id, sender_type, receiver_id, receiver_type, conversation_id, content)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (sender_id, sender_type, receiver_id, receiver_type, conversation_id, content)
        
        cursor = self.db.cursor()
        cursor.execute(query, values)
        self.db.commit()
        cursor.close()
        return conversation_id
    
    def get_conversations(self, user_id, user_type):
        """Get all conversations for a user with latest message info"""
        query = """
        SELECT m.*,
            CASE 
                WHEN m.sender_id = %s THEN m.receiver_id 
                ELSE m.sender_id 
            END as other_id,
            CASE 
                WHEN m.sender_type = %s THEN m.receiver_type 
                ELSE m.sender_type 
            END as other_type
        FROM messages m
        INNER JOIN (
            SELECT conversation_id, MAX(sent_at) as max_time
            FROM messages
            WHERE (sender_id = %s AND sender_type = %s) 
               OR (receiver_id = %s AND receiver_type = %s)
            GROUP BY conversation_id
        ) AS latest ON m.conversation_id = latest.conversation_id AND m.sent_at = latest.max_time
        ORDER BY m.sent_at DESC
        """
        
        params = (user_id, user_type, user_id, user_type, user_id, user_type)
        cursor = self.db.cursor(dictionary=True)
        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()
        
        conversations = []
        for row in results:
            conversations.append({
                'conversation_id': row['conversation_id'],
                'other_id': row['other_id'],
                'other_type': row['other_type'],
                'last_message': row['content'],
                'timestamp': row['sent_at'],
                'is_read': row['is_read']
            })
        return conversations
    
    def get_user_info(self, user_id, user_type):
        """Get user information by ID and type"""
        if user_type.lower() == 'employer':
            query = """
            SELECT employer_id as id, company_name as name, industry 
            FROM employers WHERE employer_id = %s
            """
        elif user_type.lower() == 'job_seeker':
            query = """
            SELECT seeker_id as id, CONCAT(first_name, ' ', last_name) as name 
            FROM job_seekers WHERE seeker_id = %s
            """
        else:
            return None
            
        cursor = self.db.cursor(dictionary=True)
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        cursor.close()
        return result
    
    def search_users(self, search_term, user_type, limit=10):
        """Search for users by name or company"""
        if user_type.lower() == 'employer':
            query = """
            SELECT employer_id as id, company_name as name, industry 
            FROM employers 
            WHERE company_name LIKE %s OR industry LIKE %s
            LIMIT %s
            """
            params = (f"%{search_term}%", f"%{search_term}%", limit)
            
        elif user_type.lower() == 'job_seeker':
            query = """
            SELECT seeker_id as id, CONCAT(first_name, ' ', last_name) as name 
            FROM job_seekers 
            WHERE first_name LIKE %s OR last_name LIKE %s OR degree LIKE %s
            LIMIT %s
            """
            params = (f"%{search_term}%", f"%{search_term}%", f"%{search_term}%", limit)
        else:
            return []
            
        cursor = self.db.cursor(dictionary=True)
        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()
        return results
    
    def get_conversation_history(self, conversation_id):
        """Get message history for a specific conversation"""
        query = """
        SELECT *, 
            CASE 
                WHEN is_read THEN 'Read' 
                ELSE 'Unread' 
            END as read_status
        FROM messages
        WHERE conversation_id = %s
        ORDER BY sent_at ASC
        """
        
        cursor = self.db.cursor(dictionary=True)
        cursor.execute(query, (conversation_id,))
        results = cursor.fetchall()
        cursor.close()
        return results
    
    def mark_as_read(self, conversation_id, user_id, user_type):
        """Mark messages as read for a conversation"""
        # Only mark as read if user is the receiver
        query = """
        UPDATE messages 
        SET is_read = 1
        WHERE conversation_id = %s
          AND receiver_id = %s
          AND receiver_type = %s
          AND is_read = 0
        """
        cursor = self.db.cursor()
        cursor.execute(query, (conversation_id, user_id, user_type))
        self.db.commit()
        cursor.close()

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'job_portal_db'
}

# Initialize messaging system
messaging = MessagingSystem(db_config)

# Send a message
# conv_id = messaging.send_message(
#     sender_id=139,
#     sender_type='job_seeker',
#     receiver_id=3,
#     receiver_type='employer',
#     content='Hello, I\'m interested in your job posting!'
# )

# Get user conversations
# conversations = messaging.get_conversations(user_id=139, user_type='job_seeker')

# Get conversation history
history = messaging.get_conversation_history('248264525675678')
print(history)
# # Search for users
employers = messaging.search_users('jem', 'employer')
seekers = messaging.search_users('jem', 'job_seeker')
print(employers)
print(seekers)