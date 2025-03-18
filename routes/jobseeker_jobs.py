from flask import Blueprint,render_template
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
from middlewares.user_access import jobseeker as job_seeker_middleware,admin,emplyer
# Create a Blueprint
jobseeker_job = Blueprint('jobseeker_job', __name__)

# Define your routes using the Blueprint
@jobseeker_job.route('/jobseeker/jobs')
@verify_user
@is_email_verified
def jobseeker_job_():
    return render_template('/pages/job_seeker/jobs.html')


# Define your routes using the Blueprint
@jobseeker_job.route('/jobseeker/jobs-interest')
@verify_user
@is_email_verified
def jobseeker_job_interest():
    return render_template('/pages/job_seeker/jobs_interest.html')