from flask import Blueprint,render_template,session,redirect
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
from middlewares.user_access import jobseeker as job_seeker_middleware,admin,emplyer
# Create a Blueprint
jobseeker = Blueprint('jobseeker', __name__)

# Define your routes using the Blueprint
@jobseeker.route('/jobseeker/dashboard')
@verify_user
@is_email_verified
def job_seeker_dashboard():
    """Render the job seeker's dashboard page.

    This route displays the main dashboard for job seekers. It requires user authentication
    and email verification before access is granted.

    Decorators:
        @verify_user: Ensures the user is authenticated
        @is_email_verified: Ensures the user's email is verified

    Returns:
        rendered template: The job seeker dashboard HTML page
    """
    return render_template("/pages/job_seeker/dashboard.html")