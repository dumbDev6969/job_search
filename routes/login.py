from flask import Blueprint, request, render_template, jsonify, session,redirect
from utils.database import get_db
from utils.pasword_hash import verify_password
from utils.email_utils import check_email_exists
from utils.otp_utils import generate_otp,send_otp_email
from sqlalchemy import text
from datetime import datetime,timedelta
from middlewares.is_user_logged_in import is_user_logged_in
# Create a Blueprint
login = Blueprint('login', __name__)

# Define your routes using the Blueprint
@login.route('/login', methods=['GET', 'POST'])
@is_user_logged_in
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
            
            # Check if user is verified
            verify_query = text("SELECT COUNT(*) as count FROM verified_users WHERE email = :email")
            verify_result = db.execute_query(verify_query, {'email': email})
            
            if not verify_result['success'] or verify_result['output'][0]['count'] == 0:
                return render_template("/auth/otp_virification.html",email=email),200
            
            # First check job seekers table
            seeker_query = text("""
                SELECT seeker_id, email, password_hash, first_name, last_name, 
                       phone, province, municipality, degree, portfolio_url 
                FROM job_seekers 
                WHERE email = :email
            """)
            
            seeker_result = db.execute_query(seeker_query, {'email': email})
            
            # Then check employers table
            employer_query = text("""
                SELECT employer_id, email, password_hash, company_name, 
                       industry, company_size, website, logo_url
                FROM employers 
                WHERE email = :email
            """)
            
            employer_result = db.execute_query(employer_query, {'email': email})
            
            # Handle job seeker login
            if seeker_result['success'] and seeker_result['output']:
                user = seeker_result['output'][0]
                
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
                    
                    # Set session data for job seeker
                    session['user_id'] = user['seeker_id']
                    session['email'] = user['email']
                    session['first_name'] = user['first_name']
                    session['last_name'] = user['last_name']
                    session['user_type'] = 'seeker'
                    session['profile'] = {
                        'phone': user['phone'],
                        'province': user['province'],
                        'municipality': user['municipality'],
                        'degree': user['degree'],
                        'portfolio_url': user['portfolio_url']
                    }
                    session.permanent = True
                    return redirect('/job_seeker/dashboard')
                    
            # Handle employer login
            elif employer_result['success'] and employer_result['output']:
                user = employer_result['output'][0]
                
                if verify_password(password, user['password_hash'].encode('utf-8')):
                    # Update last_login timestamp
                    update_query = text("""
                        UPDATE employers 
                        SET last_login = :timestamp 
                        WHERE employer_id = :user_id
                    """)
                    
                    db.execute_query(update_query, {
                        'timestamp': datetime.now(),
                        'user_id': user['employer_id']
                    })
                    
                    # Set session data for employer
                    session['user_id'] = user['employer_id']
                    session['email'] = user['email']
                    session['company_name'] = user['company_name']
                    session['user_type'] = 'employer'
                    session['profile'] = {
                        'industry': user['industry'],
                        'company_size': user['company_size'],
                        'website': user['website'],
                        'logo_url': user['logo_url']
                    }
                    session.permanent = True
                    return redirect("/pages/recruiter/dashboard.html")
            
            # Invalid credentials
            print('Invalid credentials')
            return jsonify({'error': 'Invalid credentials'}), 401
                
        except Exception as e:
            print(str(e))
            return jsonify({'error': 'Login failed', 'details': str(e)}), 500
            
    else:
        # Render the login form
        return render_template('auth/login.html')