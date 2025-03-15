from flask import Blueprint, request, jsonify,render_template,session,redirect
import random
import uuid
from utils.database import get_db
from utils.email_utils import check_email_exists
from datetime import datetime, timedelta


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
        stored_otp = session.get('otp', {}).get('code')
        if not stored_otp:
            return jsonify({'verified': False}), 200
            
        if stored_otp == user_otp:
            # if check_email_exists('employers', 'email', email) or check_email_exists('job_seekers', 'email', email):
            #     return jsonify({'error': 'Email already exists'}), 400
            # Remove the used OTP
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
    print("generate")
    try:
        # Get email from request
        email = request.form.get("email")
        print(f"Data: {email}")
        print(f"Form: {request.form}")
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        # if check_email_exists('employers', 'email', email) or check_email_exists('job_seekers', 'email', email):
        #     return jsonify({'error': 'Email already exists'}), 400
        # Generate 6 random numbers
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        session['otp'] = {
            'email': email,
            'code': code,
            'expiry': datetime.now() + timedelta(minutes=5)}
        # Generate unique UUID
        unique_id = str(uuid.uuid4())
        
       
        
        # Send OTP via email
        from utils.email_sender import my_send_email, SENDER_EMAIL, SENDER_PASSWORD
        
        subject = "Your OTP Code"
        body = f"Your OTP code is: {code}"
        try:
            my_send_email(subject, body, SENDER_EMAIL, [email], SENDER_PASSWORD)
            return jsonify({'success': True, 'uuid': unique_id}), 200
        except Exception as e:
            print(f"Failed to send OTP email: {str(e)}")
            return jsonify({'error': f'Failed to send OTP: {str(e)}'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 400
