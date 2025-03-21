from flask import Blueprint,render_template
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
from middlewares.user_access import jobseeker as job_seeker_middleware,admin,emplyer
# Create a Blueprint
jobseeker_find_job = Blueprint('jobseeker_find_job', __name__)

# Define your routes using the Blueprint
@jobseeker_find_job.route('/jobseeker/find-jobs')
@verify_user
@is_email_verified
def jobseeker_find_job_():
    return render_template('/pages/job_seeker/find_jobs.html')