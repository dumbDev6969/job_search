from flask import Blueprint,render_template
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
# Create a Blueprint
applicants = Blueprint('applicants', __name__)

# Define your routes using the Blueprint
@applicants.route('/employer/applicants')
@verify_user
@is_email_verified
def applicants_():
    return render_template('/pages/recruiter/applicants.html')