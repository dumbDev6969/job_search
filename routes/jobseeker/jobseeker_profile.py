from flask import Blueprint,render_template
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
from middlewares.user_access import jobseeker as job_seeker_middleware,admin,emplyer
# Create a Blueprint
jobseeker_profile= Blueprint('jobseeker_profile', __name__)

# Define your routes using the Blueprint
@jobseeker_profile.route('/jobseeker/profile')
@verify_user
@is_email_verified
def jobseeker_profile_():
    """Render the job seeker's profile page.

    This route displays the profile page for job seekers where they can view their
    personal information and profile details. Access requires user authentication
    and email verification.

    Decorators:
        @verify_user: Ensures the user is authenticated
        @is_email_verified: Ensures the user's email is verified

    Returns:
        rendered template: The job seeker profile HTML page
    """
    return render_template('/pages/job_seeker/profile.html')


@jobseeker_profile.route('/jobseeker/profile-setting')
@verify_user
@is_email_verified
def jobseeker_profile_settings():
    """Render the job seeker's profile settings page.

    This route displays the settings page where job seekers can modify their
    profile information and preferences. Access requires user authentication
    and email verification.

    Decorators:
        @verify_user: Ensures the user is authenticated
        @is_email_verified: Ensures the user's email is verified

    Returns:
        rendered template: The job seeker profile settings HTML page
    """
    return render_template('/pages/job_seeker/profile_settings.html')