from flask import Blueprint, request, render_template, jsonify, url_for, session
from utils.database import get_db
from utils.email_utils import send_reset_password_email
from sqlalchemy import text
from datetime import datetime, timedelta
import secrets

forgot_password = Blueprint('forgot_password', __name__)

@forgot_password.route('/reset-password/<token>', methods=['GET'])
def reset_password(token):
    if not token:
        return jsonify({'error': 'Invalid reset token'}), 400
    return render_template('auth/reset_password.html', token=token)

@forgot_password.route('/reset-password', methods=['POST'])
def handle_reset_password():
    try:
        data = request.get_json()
        token = data.get('token')
        new_password = data.get('password')
        
        if not token or not new_password:
            return jsonify({'error': 'Token and new password are required'}), 400
            
        db = get_db()
        
        # Verify token and check expiration
        verify_token_query = text("""
            SELECT email, expiry 
            FROM password_reset_tokens 
            WHERE token = :token
            ORDER BY created_at DESC
            LIMIT 1
        """)
        
        result = db.execute_query(verify_token_query, {'token': token})
        
        if not result['success'] or not result['output']:
            return jsonify({'error': 'Invalid or expired reset token'}), 400
            
        token_data = result['output'][0]
        if datetime.now() > token_data['expiry']:
            return jsonify({'error': 'Reset token has expired'}), 400
            
        email = token_data['email']
        
        # Hash the new password
        from utils.pasword_hash import hash_password
        password_hash = hash_password(new_password)
        
        # Update password in appropriate table based on user type
        update_seeker_query = text("""
            UPDATE job_seekers 
            SET password_hash = :password_hash 
            WHERE email = :email
        """)
        
        update_employer_query = text("""
            UPDATE employers 
            SET password_hash = :password_hash 
            WHERE email = :email
        """)
        
        # Try updating both tables (only one will be affected)
        params = {'email': email, 'password_hash': password_hash}
        seeker_result = db.execute_query(update_seeker_query, params)
        employer_result = db.execute_query(update_employer_query, params)
        
        if not seeker_result['success'] and not employer_result['success']:
            return jsonify({'error': 'Failed to update password'}), 500
            
        # Delete used token
        delete_token_query = text("DELETE FROM password_reset_tokens WHERE token = :token")
        db.execute_query(delete_token_query, {'token': token})
        
        return jsonify({'message': 'Password has been reset successfully'}), 200
        
    except Exception as e:
        print(f"Failed to reset password: {str(e)}")
        return jsonify({'error': str(e)}), 500

@forgot_password.route('/forgot-password', methods=['GET', 'POST'])
def handle_forgot_password():
    if request.method == 'GET':
        return render_template('auth/forgot_password.html')
    
    if request.method == 'POST':
        try:
            data = request.get_json()
            email = data.get('email')
            
            if not email:
                return jsonify({'error': 'Email is required'}), 400

            db = get_db()
            
            # Check if email exists in either job_seekers or employers table
            check_email_query = text("""
                SELECT 
                    CASE    
                        WHEN EXISTS (SELECT 1 FROM job_seekers WHERE email = :email) THEN 'seeker'
                        WHEN EXISTS (SELECT 1 FROM employers WHERE email = :email) THEN 'employer'
                        ELSE NULL
                    END as user_type
            """)
            
            result = db.execute_query(check_email_query, {'email': email})
            
            if not result['success'] or not result['output'][0]['user_type']:
                return jsonify({'error': 'Email not found'}), 404

            # Generate secure reset token
            reset_token = secrets.token_urlsafe(32)
            expiry = datetime.now() + timedelta(hours=24)

            # Store reset token in database
            store_token_query = text("""
                INSERT INTO password_reset_tokens (email, token, expiry)
                VALUES (:email, :token, :expiry)
            """)
            
            token_result = db.execute_query(store_token_query, {
                'email': email,
                'token': reset_token,
                'expiry': expiry
            })

            if not token_result['success']:
                return jsonify({'error': 'Failed to generate reset token'}), 500

            # Send reset password email
            reset_link = url_for('forgot_password.reset_password', token=reset_token, _external=True)
            try:
                is_email_sent = send_reset_password_email(email, reset_link)
                if not is_email_sent:
                    return jsonify({'error': 'Failed to send reset email'}), 500
                
                return jsonify({
                    'message': 'Password reset link has been sent to your email'
                }), 200

            except Exception as e:
                print(f"Failed to send reset email: {str(e)}")
                return jsonify({'error': f'Failed to send reset email: {str(e)}'}), 500
            
        except Exception as e:
            print(f"Failed to handle forgot password: {str(e)}")
            return jsonify({'error': str(e)}), 500

