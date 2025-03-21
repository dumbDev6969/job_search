from flask import Blueprint, request, jsonify,render_template,session,redirect
import random
import uuid
from utils.database import get_db
from utils.email_utils import check_email_exists
from datetime import datetime, timedelta, timezone


# Create a Blueprint
otp = Blueprint('otp', __name__)


@otp.route('/verify-account', methods=['POST'])
def verify_account():
    # Get email from either query parameters (GET) or form data (POST)
    email =  request.form.get('email')
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
        
    # Generate OTP and get UUID
    data = {'email': email}
    response = generate()
    if response[1] != 200:
        return response
        
    uuid = response[0].get_json()['uuid']
    return render_template('/auth/otp_virification.html', email=email, uuid=uuid)

# Define your routes using the Blueprint
@otp.route('/verify', methods=['POST'])
def verify() -> dict:
    try:
        # Get UUID and OTP from form data
        uuid = request.form.get('uuid')
        user_otp = request.form.get('otp')
        email = request.form.get('email')
        print(f"UUID: {uuid}, OTP: {user_otp}")
       
        # Validate required fields
        if not user_otp:
            return jsonify({'error': 'Missing required fields', 'verified': False}), 400
        
        # Check if UUID exists and OTP matches
        otp_data = session.get('otp', {})
        stored_otp = otp_data.get('code')
        expiry_time = otp_data.get('expiry')
        
        if not stored_otp or not expiry_time:
            return jsonify({'verified': False}), 200
            
        # Check if OTP has expired
        current_time = datetime.now(timezone.utc)
        if current_time > expiry_time:
            session.pop('otp', None)
            return jsonify({'error': 'OTP has expired', 'verified': False}), 400
            
        if stored_otp == user_otp:
            session.pop('otp', None)
            db = get_db()
            from sqlalchemy import text
            query = text("INSERT INTO verified_users (email) VALUES (:email)")
            result = db.execute_query(query, {'email': email})
            if not result['success']:
                return jsonify({'error': f'Failed to verify user: {result["message"]}'}), 500
            print(f"Successfully verified user {email}")
            return jsonify({'verified': True}), 200
        
        return jsonify({'verified': False}), 200
    except Exception as e:
        return jsonify({'error': str(e), 'verified': False}), 400

@otp.route('/generate', methods=['POST'])
def generate() -> dict:
    try:
        # Get email from request
        email = request.form.get("email")
        if not email:
            return jsonify({'error': 'Email is required'}), 400
            
        # Rate limiting check
        last_request = session.get('last_otp_request', {})
        # print(last_request)
        # if email in last_request:
        #     current_time = datetime.now(timezone.utc)
        #     last_request_time = last_request[email]
        #     time_diff = (current_time - last_request_time).total_seconds()
        #     if time_diff < 60:  # 1 minute cooldown
        #         return jsonify({'error': f'Please wait {60 - int(time_diff)} seconds before requesting another OTP'}), 429

        # Generate 6 random numbers
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        
        # Store OTP data with timezone-aware datetime
        session['otp'] = {
            'email': email,
            'code': code,
            'expiry': datetime.now(timezone.utc) + timedelta(minutes=5)
        }
        
        # Update rate limiting with timezone-aware datetime
        if 'last_otp_request' not in session:
            session['last_otp_request'] = {}
        session['last_otp_request'][email] = datetime.now(timezone.utc)
        
        # Generate unique UUID
        unique_id = str(uuid.uuid4())
        
        # Send OTP via email
        from utils.email_sender import my_send_email
        
        subject = "Your OTP Verification Code"
        body = f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2>Email Verification</h2>
            <p>Your verification code is:</p>
            <h1 style="color: #4CAF50; font-size: 32px; letter-spacing: 5px;">{code}</h1>
            <p>This code will expire in 5 minutes.</p>
            <p>If you didn't request this code, please ignore this email.</p>
        </body>
        </html>
        """
        
        try:
            my_send_email(subject, body, [email])
            return jsonify({'success': True, 'uuid': unique_id}), 200
        except Exception as e:
            return jsonify({'error': f'Failed to send OTP: {str(e)}'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 400
