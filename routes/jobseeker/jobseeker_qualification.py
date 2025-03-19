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
    """Render the job seeker's qualification page.

    This route displays the page where job seekers can view and manage their
    qualifications, skills, and experience. Access requires user authentication
    and email verification.

    Decorators:
        @verify_user: Ensures the user is authenticated
        @is_email_verified: Ensures the user's email is verified

    Returns:
        rendered template: The job seeker qualification HTML page
    """
    return render_template('/pages/job_seeker/qualification.html')