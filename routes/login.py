from flask import Blueprint, request, render_template, jsonify, session, redirect
from utils.database import get_db
from utils.pasword_hash import verify_password
from utils.email_utils import check_email_exists
from utils.otp_utils import generate_otp, send_otp_email
from sqlalchemy import text
from datetime import datetime, timedelta
from middlewares.is_user_logged_in import is_user_logged_in

# Create a Blueprint
login = Blueprint('login', __name__)

# Define your routes using the Blueprint
@login.route('/login', methods=['GET', 'POST'])
@is_user_logged_in
def login_user():
    """
    Handle user login functionality.
    
    GET: Renders the login form
    POST: Processes login attempt
    
    Form Parameters:
        - email (str): User's email address
        - password (str): User's password
    
    Returns:
        - GET: Rendered login template
        - POST (success): Redirect to appropriate dashboard
        - POST (failure): JSON error response with appropriate status code
    """
    if request.method == 'POST':
        form = request.form
        email = form.get('email')
        password = form.get('password')
        
        if not email or not password:
            logging.error('Email and password are required but not provided')
            return jsonify({'error': 'Email and password are required'}), 400
            
        try:
            # Get database connection
            db = get_db()
            logging.info('Checking if email exists in the database')
            check_email_query = text("""
                SELECT 
                    CASE    
                        WHEN EXISTS (SELECT 1 FROM job_seekers WHERE email = :email) THEN 1
                        WHEN EXISTS (SELECT 1 FROM employers WHERE email = :email) THEN 1
                        WHEN EXISTS (SELECT 1 FROM admin WHERE email = :email) THEN 1
                        ELSE 0
                    END as email_exists
            """)
            
            email_check_result = db.execute_query(check_email_query, {'email': email})
            logging.info(f"Email check result: {email_check_result}")
            if not email_check_result['success'] or not email_check_result['output'][0]['email_exists']:
                logging.warning(f"Email {email} does not exist")
                return jsonify({'error': 'Email does not exist'}), 404
            
            logging.info('Checking if user is verified')
            verify_query = text("SELECT COUNT(*) as count FROM verified_users WHERE email = :email")
            verify_result = db.execute_query(verify_query, {'email': email})
            
            # First check if email exists in either table
            # First check job seekers table
            logging.info('Checking for job seeker login')
            seeker_query = text("""
                SELECT seeker_id, email, password_hash, first_name, last_name, 
                       phone, province, municipality, degree, portfolio_url 
                FROM job_seekers 
                WHERE email = :email
            """)
            
            seeker_result = db.execute_query(seeker_query, {'email': email})
            
            # Then check employers table
            logging.info('Checking for employer login')
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
                    logging.info(f"Job seeker {user['email']} verified")
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
                    logging.info('Redirecting to job seeker dashboard')
                    return redirect("/dashboard")
                    
            # Handle employer login
            elif employer_result['success'] and employer_result['output']:
                user = employer_result['output'][0]
                
                if verify_password(password, user['password_hash'].encode('utf-8')):
                    logging.info(f"Employer {user['email']} verified")
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
                    logging.info('Redirecting to employer dashboard')
                    return redirect("/dashboard")
            
            else:
                logging.info("Checking admin credentials")
                admin_query = text("""
                    SELECT username, email, password
                    FROM admin 
                    WHERE email = :email
                """)
    
                admin_result = db.execute_query(admin_query, {'email': email})
                logging.info(f"Admin result: {admin_result}")
                
                if admin_result['success'] and admin_result['output']:
                    user = admin_result['output'][0]
                    logging.info(f"Admin login attempt with email: {email}")
                    
                    if verify_password(password, user['password']):
                        logging.info("Admin verified")
                        # Set session data for admin
                        session['user_id'] = user['username']
                        session['email'] = user['email']
                        session['username'] = user['username']
                        session['user_type'] = 'admin'
                        session.permanent = True
                        logging.info('Redirecting to admin index')
                        return redirect("/admin/index")
                
            logging.error('Invalid credentials provided')
            return jsonify({'error': 'Invalid credentials'}), 401
            
        except Exception as e:
            logging.error(f"Login failed with error: {str(e)}")
            return jsonify({'error': 'Login failed', 'details': str(e)}), 500
            
    else:
        logging.info("Rendering login form")
        return render_template('auth/login.html')
