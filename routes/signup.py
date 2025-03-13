from flask import Blueprint, request, render_template, jsonify, current_app as app,redirect
from utils.database import get_db
from utils.pasword_hash import hash_password
from utils.email_utils import check_email_exists
from sqlalchemy import text
from werkzeug.utils import secure_filename
import os

# Configure upload settings
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Create a Blueprint
signup = Blueprint('signup', __name__)

# Define your routes using the Blueprint
@signup.route('/signup', methods=['GET', 'POST'])
def confirm_role():
    return render_template('auth/confirm-role.html')

@signup.route('/signup/employer', methods=['GET', 'POST'])
def signup_employer():
    if request.method == 'POST':
        form = request.form
        
        # Extract form data
        email = form.get('email')
        
        # Check if email already exists
        if check_email_exists('employers', 'email', email):
            return jsonify({'error': 'Email already exists'}), 400
            
        password = form.get('password')
        company_name = form.get('company_name')
        industry = form.get('industry')
        company_size = form.get('company_size')
        website = form.get('website')
        
        # Handle file upload for logo
        logo_file = request.files.get('logo_url')
        logo_url = ''
        if logo_file and allowed_file(logo_file.filename):
            filename = secure_filename(logo_file.filename)
            logo_url = f'/uploads/logos/{filename}'
            logo_file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'logos', filename))
        
        # Hash the password
        password_hash = hash_password(password)
        
        try:
            # Get database connection
            db = get_db()
            
            # Insert employer data
            query = text("""
                INSERT INTO employers 
                (email, password_hash, company_name, industry, company_size, website, logo_url)
                VALUES 
                (:email, :password_hash, :company_name, :industry, :company_size, :website, :logo_url)
            """)
            
            result = db.execute_query(query, {
                'email': email,
                'password_hash': password_hash,
                'company_name': company_name,
                'industry': industry,
                'company_size': company_size,
                'website': website,
                'logo_url': logo_url
            })
            
            if result['success']:
                return redirect("/login")
                return jsonify({'message': 'Registration successful'}), 201
            else:
                return jsonify({'error': 'Registration failed', 'details': result['message']}), 400
                
        except Exception as e:
            return jsonify({'error': 'Registration failed', 'details': str(e)}), 500
            
    else:
        # Render the signup form
        return render_template('auth/register_employers.html')

@signup.route('/signup/jobseeker', methods=['GET', 'POST'])
def signup_jobseeker():
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
        if check_email_exists('job_seekers', 'email', email):
            return jsonify({'success': False, 'error': 'Email already exists'}), 400
            
        password = data.get('password')
        if not password:
            return jsonify({'success': False, 'error': 'Password is required'}), 400
            
        first_name = data.get('name')
        last_name = data.get('las-name')
        phone = data.get('phone')
        province = data.get('province')
        municipality = data.get('municipality')
        degree = data.get('degree')
        portfolio = data.get('portfolio')
        
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
                'portfolio': portfolio
            })
            
            if result['success']:
                return jsonify({
                    'success': True,
                    'message': 'Registration successful'
                })
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