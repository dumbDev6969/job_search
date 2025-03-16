from flask import Blueprint,render_template,session,redirect
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
from middlewares.user_access import jobseeker,admin,emplyer

# Create a Blueprint
dashboard = Blueprint('dashboard', __name__)

# Define your routes using the Blueprint
@dashboard.route('/dashboard')
@verify_user
@is_email_verified
def dashboard_():
    if session.get('user_type') == 'jobseeker':
        return redirect('/job_seeker/dashboard')
    elif session.get('user_type') == 'employer':
        return redirect('/employer/dashboard')
    elif session.get('user_type') == 'admin':
        return redirect('/admin/dashboard')
    else:
        return redirect('/login')