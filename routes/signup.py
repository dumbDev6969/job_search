from flask import Blueprint, request, render_template, flash, redirect, url_for
from utils.database import get_db

# Create a Blueprint
signup = Blueprint('signup', __name__)

# Define your routes using the Blueprint
@signup.route('/signup', methods=['GET', 'POST'])
def signup_jobseeker():
    if request.method == 'POST':
        db = get_db()
        result = db.insert_job_seeker(request.form)
        
        if result['success']:
            flash('Registration successful!', 'success')
            return redirect(url_for('login'))
        else:
            flash(result['message'], 'error')
            return render_template('auth/register.html')
    else:
        # Render the signup form
        return render_template('auth/register.html')