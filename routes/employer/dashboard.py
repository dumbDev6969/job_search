
from flask import Blueprint,render_template
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
# Create a Blueprint
dashboard = Blueprint('dashboard', __name__)

# Define your routes using the Blueprint
@dashboard.route('/employer/dashboard')
@verify_user
@is_email_verified
def dashboard_():
    return render_template('/pages/recruiter/dashboard.html')