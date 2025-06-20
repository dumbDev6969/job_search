import random
import string
from datetime import datetime, timedelta
from .email_sender import my_send_email
from .database import DatabaseManager
from sqlalchemy import text
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get email credentials
SENDER_EMAIL = os.getenv('SENDER_EMAIL')
SENDER_PASSWORD = os.getenv('SENDER_PASSWORD')

def generate_otp(length=6):
    """Generate a random OTP of specified length"""
    logger = logging.getLogger('generate_otp')
    logger.info(f"Generating OTP of length {length}")
    
    digits = string.digits
    otp = ''.join(random.choice(digits) for _ in range(length))
    logger.info(f"Generated OTP: {otp}")
    return otp

def save_otp(email: str, otp: str, expiry_minutes: int = 10):
    """Save OTP to database with expiration time"""
 
    
    try:
        db = DatabaseManager('mysql', 'mysql+pymysql://root@localhost/job_portal_db')
        expiry_time = datetime.now() + timedelta(minutes=expiry_minutes)
        
        # First, invalidate any existing OTPs for this email
        invalidate_query = text("UPDATE otp_codes SET is_valid = FALSE WHERE email = :email")
        logger.info(f"Invalidate existing OTPs for email {email}")
        db.execute_query(invalidate_query, {'email': email})
        
        # Insert new OTP
        insert_query = text("""
            INSERT INTO otp_codes (email, otp_code, expiry_time, is_valid)
            VALUES (:email, :otp, :expiry_time, TRUE)
        """)
        
        logger.info(f"Saving OTP {otp} for email {email}")
        result = db.execute_query(insert_query, {
            'email': email,
            'otp': otp,
            'expiry_time': expiry_time
        })
        
        if result['success']:
            logger.info(f"OTP saved for email {email}")
        else:
            logger.error(f"Error saving OTP for email {email}")
        
        return result['success']
    except Exception as e:
        logger.error(f"Error saving OTP: {str(e)}")
        return False
    finally:
        if 'db' in locals():
            db.close()

def verify_otp(email: str, otp: str) -> bool:
    """Verify if OTP is valid and not expired"""
    try:
        db = DatabaseManager('mysql', 'mysql+pymysql://root@localhost/job_portal_db')
        query = text("""
            SELECT COUNT(*) as count 
            FROM otp_codes 
            WHERE email = :email 
            AND otp_code = :otp 
            AND is_valid = TRUE 
            AND expiry_time > NOW()
        """)
        
        logger.info(f"Checking OTP for {email}")
        
        result = db.execute_query(query, {'email': email, 'otp': otp})
        
        if result['success']:
            count = result['output'][0]['count']
            if count > 0:
                # Invalidate the used OTP
                invalidate_query = text("""
                    UPDATE otp_codes 
                    SET is_valid = FALSE 
                    WHERE email = :email AND otp_code = :otp
                """)
                logger.info(f"Invalidating OTP for {email}")
                db.execute_query(invalidate_query, {'email': email, 'otp': otp})
                return True
            else:
                logger.info(f"OTP for {email} is invalid")
        else:
            logger.error(f"Error checking OTP for {email}")
        
        return False
    except Exception as e:
        logger.error(f"Error verifying OTP for {email}: {str(e)}")
        return False
    finally:
        if 'db' in locals():
            db.close()

def send_otp_email(email: str, otp: str) -> bool:
    """Generate and send OTP via email"""
    try:
        if save_otp(email, otp):
            subject = "Your OTP Code"
            body = f"Your OTP code is: {otp}\n\nThis code will expire in 10 minutes."
            
            my_send_email(
                subject=subject,
                body=body,
                sender=SENDER_EMAIL,
                recipients=[email],
                password=SENDER_PASSWORD
            )
            print(f"OTP email sent successfully to {email}")
            logging.debug(f"Sent OTP email to {email}")
            return True
        logging.error("Failed to save OTP")
        return False
    except Exception as e:
        logging.error(f"Error sending OTP email: {str(e)}")
        return False


