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
    return render_template('/pages/job_seeker/profile.html')


@jobseeker_profile.route('/jobseeker/profile-setting')
@verify_user
@is_email_verified
def jobseeker_profile_settings():
    return render_template('/pages/job_seeker/profile_settings.html')