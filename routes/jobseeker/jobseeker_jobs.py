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
    """Render the job seeker's jobs page.

    This route displays the page where job seekers can view available job listings
    and opportunities. Access requires user authentication and email verification.

    Decorators:
        @verify_user: Ensures the user is authenticated
        @is_email_verified: Ensures the user's email is verified

    Returns:
        rendered template: The job seeker jobs HTML page
    """
    return render_template('/pages/job_seeker/jobs.html')


@jobseeker_job.route('/jobseeker/jobs-interest')
@verify_user
@is_email_verified
def jobseeker_job_interest():
    """Render the job seeker's job interests page.

    This route displays the page where job seekers can view and manage their
    saved job interests. Access requires user authentication and email verification.

    Decorators:
        @verify_user: Ensures the user is authenticated
        @is_email_verified: Ensures the user's email is verified

    Returns:
        rendered template: The job seeker job interests HTML page
    """
    return render_template('/pages/job_seeker/job_interests.html')