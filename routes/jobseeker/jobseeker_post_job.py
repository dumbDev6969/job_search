from flask import Blueprint,render_template
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
from middlewares.user_access import jobseeker as job_seeker_middleware,admin,emplyer
from middlewares.is_setup_done import is_interests_done,is_qualification_done

# Create a Blueprint
jobseeker_post_job = Blueprint('jobseeker_post_job', __name__)

# Define your routes using the Blueprint
@jobseeker_post_job.route('/jobseeker/post-job')
@verify_user
@is_email_verified
@is_qualification_done
@job_seeker_middleware
def jobseeker_post_job_():
    """Render the job seeker's post job page.

    This route displays the page where job seekers can create and post new job
    listings. Access requires user authentication and email verification.

    Decorators:
        @verify_user: Ensures the user is authenticated
        @is_email_verified: Ensures the user's email is verified

    Returns:
        rendered template: The job seeker post job HTML page
    """
    return render_template('/pages/job_seeker/post_job.html')