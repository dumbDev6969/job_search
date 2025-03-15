from flask import Blueprint,render_template,session,redirect
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified

# Create a Blueprint
jobseeker = Blueprint('jobseeker', __name__)

# Define your routes using the Blueprint
@jobseeker.route('/job_seeker/dashboard')
@verify_user
@is_email_verified
def job_seeker_dashboard():
    return render_template("/pages/job_seeker/dashboard.html")