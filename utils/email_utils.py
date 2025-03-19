from utils.database import DatabaseManager
from sqlalchemy import text
from .email_sender import my_send_email, SENDER_EMAIL, SENDER_PASSWORD

def check_email_exists(table_name: str, email_column: str, email: str) -> bool:
    """
    Check if an email exists in a specified table and column.
    
    Args:
        table_name (str): The name of the table to check
        email_column (str): The name of the email column in the table
        email (str): The email address to check
        
    Returns:
        bool: True if email exists, False otherwise
    """
    try:
        db = DatabaseManager('mysql', 'mysql+pymysql://root@localhost/job_portal_db')
        query = text(f"SELECT COUNT(*) as count FROM {table_name} WHERE {email_column} = :email")
        
        # Execute the query with parameters dictionary
        result = db.execute_query(query, {'email': email})
        
        if not result['success']:
            print(f"Query execution failed: {result['message']}")
            return False
            
        # Safely access the count value
        if result['output'] and len(result['output']) > 0:
            count = result['output'][0]['count']
            return count > 0
        
        return False
        
    except Exception as e:
        print(f"Error checking email existence: {str(e)}")
        return False
    finally:
        if 'db' in locals():
            db.close()

def send_reset_password_email(email, reset_link):
    """
    Send a password reset email to the user with a secure reset link.
    
    Args:
        email (str): The recipient's email address
        reset_link (str): The password reset link
        
    Returns:
        bool: True if email was sent successfully, False otherwise
    """
    try:
        subject = "Password Reset Request"
        # Create HTML email body
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c3e50;">Password Reset Request</h2>
                <p>Hello,</p>
                <p>We received a request to reset your password. Click the link below to set a new password:</p>
                <p style="margin: 25px 0;">
                    <a href="{reset_link}" style="background-color: #3498db; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px;">
                        Reset Password
                    </a>
                </p>
                <p>If you didn't request this password reset, you can safely ignore this email.</p>
                <p>This link will expire in 24 hours.</p>
                <p>Best regards,<br>Your Support Team</p>
            </div>
        </body>
        </html>
        """
        
        # Send the email
        my_send_email(subject, body, SENDER_EMAIL, [email], SENDER_PASSWORD)
        return True
        
    except Exception as e:
        print(f"Error sending reset password email: {str(e)}")
        return False


