
from flask import Blueprint,render_template
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
# Create a Blueprint
jobs = Blueprint('jobs', __name__)

# Define your routes using the Blueprint
@jobs.route('/employer/jobs')
@verify_user
@is_email_verified
def jobs_():
    return render_template('/pages/recruiter/jobs.html')