from flask import Blueprint,render_template
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
# Create a Blueprint
find_talent = Blueprint('find_talent', __name__)

# Define your routes using the Blueprint
@find_talent.route('/employer/find-talent')
@verify_user
@is_email_verified
def find_talent_():
    return render_template('/pages/recruiter/find_talent.html')