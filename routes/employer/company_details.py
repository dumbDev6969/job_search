

from flask import Blueprint,render_template
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
# Create a Blueprint
company_details = Blueprint('company_details', __name__)

# Define your routes using the Blueprint
@company_details.route('/employer/company-details')
@verify_user
@is_email_verified
def company_details_():
    return render_template('/pages/recruiter/company_details.html')