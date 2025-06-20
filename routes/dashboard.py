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
    """
    Dashboard route that redirects to the user's respective dashboard based on their user type
    """
    if session.get('user_type') == 'jobseeker':
        logging.info(f"Redirecting job seeker {session.get('email')} to find jobs page")
        return redirect('/jobseeker/find-jobs')
    elif session.get('user_type') == 'employer':
        logging.info(f"Redirecting employer {session.get('email')} to employer dashboard")
        return redirect('/employer/dashboard')
    elif session.get('user_type') == 'admin':
        logging.info(f"Redirecting admin {session.get('email')} to admin dashboard")
        return redirect('/admin/dashboard')
    else:
        logging.warning("User type not found in session, redirecting to login")
        return redirect('/login')