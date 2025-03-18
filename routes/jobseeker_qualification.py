from flask import Blueprint,render_template
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
from middlewares.user_access import jobseeker as job_seeker_middleware,admin,emplyer
# Create a Blueprint
jobseeker_qualification = Blueprint('jobseeker_qualification', __name__)

# Define your routes using the Blueprint
@jobseeker_qualification.route('/jobseeker/qualification')
@verify_user
@is_email_verified
def jobseeker_qualification_():
    return render_template('/pages/job_seeker/qualification.html')