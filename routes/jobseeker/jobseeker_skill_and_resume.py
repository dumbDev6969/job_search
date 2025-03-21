from flask import Blueprint,render_template
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
from middlewares.user_access import jobseeker as jobseeker,admin,emplyer
from middlewares.is_setup_done import is_interests_done,is_qualification_done

# Create a Blueprint
jobseeker_skill_and_resume = Blueprint('jobseeker_profile', __name__)

# Define your routes using the Blueprint
@jobseeker_skill_and_resume.route('/jobseeker/profile')
@verify_user
@is_email_verified
@is_qualification_done
@is_interests_done
def jobseeker_skill_and_resume_():
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
    return render_template('/pages/job_seeker/skills_resume.html')