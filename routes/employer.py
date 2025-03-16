from flask import Blueprint,render_template,session,redirect
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
from middlewares.user_access import jobseeker,admin,emplyer

# Create a Blueprint
employer = Blueprint('employer', __name__)

# Define your routes using the Blueprint
@employer.route('/employer/dashboard')
@verify_user
@is_email_verified

def employer_dashboard():
    return render_template("/pages/recruiter/dashboard.html")





