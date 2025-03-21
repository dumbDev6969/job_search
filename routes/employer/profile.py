from flask import Blueprint,render_template
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
# Create a Blueprint
profile = Blueprint('profile', __name__)

# Define your routes using the Blueprint
@profile.route('/employer/profile')
@verify_user
@is_email_verified
def profile_():
    return render_template('/pages/recruiter/profile.html')