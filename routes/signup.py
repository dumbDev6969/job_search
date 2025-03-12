from flask import Blueprint, request, render_template, jsonify
from utils.database import get_db
from utils.pasword_hash import hash_password
from utils.email_utils import check_email_exists
from sqlalchemy import text
import os

# Create a Blueprint
signup = Blueprint('signup', __name__)

# Define your routes using the Blueprint
@signup.route('/signup', methods=['GET', 'POST'])
def signup_jobseeker():
    if request.method == 'POST':
        form = request.form
        
        # Extract form data
        email = form.get('email')
        
        # Check if email already exists
        if check_email_exists('job_seekers', 'email', email):
            return jsonify({'error': 'Email already exists'}), 400
            
        password = form.get('password')
        first_name = form.get('name')
        last_name = form.get('las-name')
        phone = form.get('phone')
        province = form.get('province')
        municipality = form.get('municipality')
        degree = form.get('degree')
        portfolio = form.get('portfolio')
        
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
            print(result)
            if result['success']:
                return jsonify({'message': 'Registration successful'}), 201
            else:
                return jsonify({'error': 'Registration failed', 'details': result['message']}), 400
                
        except Exception as e:
            return jsonify({'error': 'Registration failed', 'details': str(e)}), 500
            
    else:
        # Render the signup form
        return render_template('auth/register.html')