

from flask import Blueprint,render_template
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
# Create a Blueprint
job_details = Blueprint('job_details', __name__)

# Define your routes using the Blueprint
@job_details.route('/employer/job_details')
@verify_user
@is_email_verified
def job_details_():
    return render_template('/pages/recruiter/job_details.html')