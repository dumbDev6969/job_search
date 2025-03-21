from utils.database import DatabaseManager
from sqlalchemy import text
from .email_sender import my_send_email

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
        # Create HTML email body with improved styling and mobile responsiveness
        body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
        </head>
        <body style="margin: 0; padding: 0; font-family: Arial, 'Helvetica Neue', Helvetica, sans-serif; line-height: 1.6; color: #333333; background-color: #f4f4f4;">
            <table role="presentation" cellpadding="0" cellspacing="0" style="width: 100%; margin: 0; padding: 0; background-color: #f4f4f4;">
                <tr>
                    <td style="padding: 20px 0;">
                        <table role="presentation" cellpadding="0" cellspacing="0" style="max-width: 600px; margin: 0 auto; padding: 20px; background-color: #ffffff; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                            <tr>
                                <td style="padding: 20px;">
                                    <h2 style="margin: 0 0 20px; color: #2c3e50; font-size: 24px; font-weight: bold;">Password Reset Request</h2>
                                    <p style="margin: 0 0 15px; font-size: 16px;">Hello,</p>
                                    <p style="margin: 0 0 20px; font-size: 16px;">We received a request to reset your password. Please click the button below to set a new password:</p>
                                    <table role="presentation" cellpadding="0" cellspacing="0" style="width: 100%; margin: 30px 0;">
                                        <tr>
                                            <td align="center">
                                                <a href="{reset_link}" style="display: inline-block; background-color: #3498db; color: #ffffff; font-size: 16px; font-weight: bold; padding: 12px 30px; text-decoration: none; border-radius: 5px; text-align: center; mso-padding-alt: 0; mso-text-raise: 15pt;">Reset Password</a>
                                            </td>
                                        </tr>
                                    </table>
                                    <p style="margin: 0 0 15px; font-size: 14px; color: #666666;">If you didn't request this password reset, you can safely ignore this email.</p>
                                    <p style="margin: 0 0 15px; font-size: 14px; color: #666666;">This link will expire in 24 hours for security reasons.</p>
                                    <hr style="border: none; border-top: 1px solid #e0e0e0; margin: 25px 0;">
                                    <p style="margin: 0; font-size: 14px; color: #666666;">Best regards,<br>Your Support Team</p>
                                </td>
                            </tr>
                        </table>
                    </td>
                </tr>
            </table>
        </body>
        </html>
        """
        
        # Send the email
        my_send_email(subject, body, [email])
        return True
        
    except Exception as e:
        print(f"Error sending reset password email: {str(e)}")
        return False


