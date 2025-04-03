

from flask import Blueprint,render_template
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
# Create a Blueprint
company_dashboard = Blueprint('company_dashboard', __name__)

# Define your routes using the Blueprint
@company_dashboard.route('/employer/company_dashboard')
@verify_user
@is_email_verified
def employer_dashboard_():
    return render_template('/pages/recruiter/company_dashboard.html')