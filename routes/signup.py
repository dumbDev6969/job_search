from flask import Blueprint, request, render_template, jsonify, current_app as app,redirect, Response,session
from utils.database import get_db
from utils.pasword_hash import hash_password
from utils.email_utils import check_email_exists
from sqlalchemy import text
from werkzeug.utils import secure_filename
from typing import Union
import os
import uuid

def generate_uuid():
    return str(uuid.uuid4())

# Configure upload settings
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Create a Blueprint
signup = Blueprint('signup', __name__)

# Define your routes using the Blueprint
@signup.route('/signup', methods=['GET', 'POST'])
@signup.route('/auth/confirm-role.html', methods=['GET', 'POST'])
def confirm_role():
    session.clear()
    return render_template('auth/confirm-role.html')

@signup.route('/signup/employer', methods=['GET', 'POST'])
def signup_employer() -> Union[Response, dict]:
    """Handle employer registration

    Methods:
        GET: Render employer registration form
        POST: Process employer registration data

    Returns:
        GET: Rendered HTML template
        POST: JSON response with success status or error details
    """
    if request.method == 'POST':
        form = request.form
        
        # Validate required fields
        required_fields = ['email', 'password', 'company_name', 'company_size']
        missing = [field for field in required_fields if not form.get(field)]
        
        if missing:
            return jsonify({'success': False, 'error': 'Missing required fields', 'missing': missing}), 400
        
        # Check email existence
        email = form.get('email')
        if check_email_exists('employers', 'email', email) or check_email_exists('job_seekers', 'email', email):
            return jsonify({'success': False, 'error': 'Email already exists'}), 400
            
        password = form.get('password')
        company_name = form.get('company_name')
        industry = form.get('industry')
        company_size = form.get('company_size')
        website = form.get('website')
        field = form.get('field')
        
        # Handle file upload for logo
        logo_file = request.files.get('logo_url')
        logo_url = ''
        if logo_file and allowed_file(logo_file.filename):
            filename = secure_filename(logo_file.filename)
            upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'logos')
            os.makedirs(upload_dir, exist_ok=True)
            try:
                logo_file.save(os.path.join(upload_dir, filename))
                logo_url = f'/uploads/logos/{filename}'
            except Exception as e:
                return jsonify({'success': False, 'error': 'File upload failed', 'details': str(e)}), 500
        
        # Hash the password
        password_hash = hash_password(password)
        
        try:
            # Get database connection
            db = get_db()
            
            # Insert employer data
            query = text("""
                INSERT INTO employers 
                (email, password_hash, company_name, industry, company_size, website, logo_url, register_id, field)
                VALUES 
                (:email, :password_hash, :company_name, :industry, :company_size, :website, :logo_url, :register_id, :field)
            """)
            uuid = generate_uuid()
            session['uuid'] = uuid
            result = db.execute_query(query, {
                'email': email,
                'password_hash': password_hash,
                'company_name': company_name,
                'industry': industry,
                'company_size': company_size,
                'website': website,
                'logo_url': logo_url,
                'register_id':uuid,
                'field': field
            })
            
            if result['success']:
                session['id_step_1_done'] = True
                print("the results::::::::::::::::::::",result) 
                return jsonify({'success': True, 'message': 'Registration successful'})
                # return redirect("/login")
                return redirect('/signup/requirements')
            else:
                print(result)
                return jsonify({'success': False, 'error': 'Registration failed', 'details': result['message']}), 400
                
        except Exception as e:
            return jsonify({'success': False, 'error': 'Registration failed', 'details': str(e)}), 500
            
    else:
        # Render the signup form
        return render_template('auth/register_employers.html')

@signup.route('/signup/jobseeker', methods=['GET', 'POST'])
def signup_jobseeker() -> Union[Response, dict]:
    """Handle job seeker registration

    Methods:
        GET: Render job seeker registration form
        POST: Process job seeker registration data

    Returns:
        GET: Rendered HTML template
        POST: JSON response with success status or error details
    """
    if request.method == 'POST':
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
        
        # Extract form data
        email = data.get('email')
        if not email:
            return jsonify({'success': False, 'error': 'Email is required'}), 400
        
        # Check if email already exists
        if check_email_exists('employers', 'email', email) or check_email_exists('job_seekers', 'email', email):
            return jsonify({'success': False, 'error': 'Email already exists'}), 400
            
        password = data.get('password')
        if not password:
            return jsonify({'success': False, 'error': 'Password is required'}), 400
            
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        phone = data.get('phone')
        province = data.get('province')
        municipality = data.get('municipality')
        degree = data.get('degree')
        
        # Handle file upload for portfolio
        portfolio_file = request.files.get('portfolio')
        portfolio_url = ''
        if portfolio_file and allowed_file(portfolio_file.filename):
            filename = secure_filename(portfolio_file.filename)
            upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], 'portfolios')
            os.makedirs(upload_dir, exist_ok=True)
            try:
                portfolio_file.save(os.path.join(upload_dir, filename))
                portfolio_url = f'/uploads/portfolios/{filename}'
            except Exception as e:
                return jsonify({'success': False, 'error': 'File upload failed', 'details': str(e)}), 500
        
        # Hash the password
        password_hash = hash_password(password)
        
        try:
            # Get database connection
            db = get_db()
            
            # Insert user data
            query = text("""
                INSERT INTO job_seekers 
                (email, password_hash, first_name, last_name, phone, province, municipality, degree, portfolio_url)
                VALUES 
                (:email, :password_hash, :first_name, :last_name, :phone, :province, :municipality, :degree, :portfolio)
            """)
            
            result = db.execute_query(query, {
                'email': email,
                'password_hash': password_hash,
                'first_name': first_name,
                'last_name': last_name,
                'phone': phone,
                'province': province,
                'municipality': municipality,
                'degree': degree,
                'portfolio': portfolio_url
            })
            
            if result['success']:
                return jsonify({
                    'success': True,
                    'message': 'Registration successful'
                }), 201
            else:
                return jsonify({
                    'success': False,
                    'error': 'Registration failed',
                    'details': result['message']
                }), 400
            
        except Exception as e:
            return jsonify({'success': False, 'error': 'Registration failed', 'details': str(e)}), 500
            
    else:
        # Render the signup form
        return render_template('auth/register_seekers.html')

