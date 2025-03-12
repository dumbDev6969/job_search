from flask import Blueprint, request, render_template, jsonify, session
from utils.database import get_db
from utils.pasword_hash import verify_password
from utils.email_utils import check_email_exists
from sqlalchemy import text
from datetime import datetime

# Create a Blueprint
login = Blueprint('login', __name__)

# Define your routes using the Blueprint
@login.route('/login', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        form = request.form
        email = form.get('email')
        password = form.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
            
        try:
            # Get database connection
            db = get_db()
            
            # Check if user exists and get their credentials
            query = text("""
                SELECT seeker_id, email, password_hash, first_name, last_name, 
                       phone, province, municipality, degree, portfolio_url 
                FROM job_seekers 
                WHERE email = :email
            """)
            
            result = db.execute_query(query, {'email': email})
            
            if result['success'] and result['output']:
                user = result['output'][0]
                
                # Verify password
                if verify_password(password, user['password_hash'].encode('utf-8')):
                    # Update last_login timestamp
                    update_query = text("""
                        UPDATE job_seekers 
                        SET last_login = :timestamp 
                        WHERE seeker_id = :user_id
                    """)
                    
                    db.execute_query(update_query, {
                        'timestamp': datetime.now(),
                        'user_id': user['seeker_id']
                    })
                    
                    # Set session data
                    session['user_id'] = user['seeker_id']
                    session['email'] = user['email']
                    session['first_name'] = user['first_name']
                    session['last_name'] = user['last_name']
                    session['profile'] = {
                        'phone': user['phone'],
                        'province': user['province'],
                        'municipality': user['municipality'],
                        'degree': user['degree'],
                        'portfolio_url': user['portfolio_url']
                    }
                    
                    return jsonify({
                        'message': 'Login successful',
                        'user': {
                            'id': user['seeker_id'],
                            'email': user['email'],
                            'name': f"{user['first_name']} {user['last_name']}"
                        }
                    }), 200
                else:
                    print('Invalid credentials')
                    return jsonify({'error': 'Invalid credentials'}), 401
            else:
                print('Invalid credentials')
                return jsonify({'error': 'Invalid credentials'}), 401
                
        except Exception as e:
            print(str(e))
            return jsonify({'error': 'Login failed', 'details': str(e)}), 500
            
    else:
        # Render the login form
        return render_template('auth/login.html')