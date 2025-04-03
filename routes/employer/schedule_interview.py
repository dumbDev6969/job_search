

from flask import Blueprint,render_template
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
# Create a Blueprint
schedule_interview = Blueprint('schedule_interview', __name__)

# Define your routes using the Blueprint
@schedule_interview.route('/employer/schedule_interview')
@verify_user
@is_email_verified
def schedule_interview_():
    return render_template('/pages/recruiter/schedule_interview.html')