

from flask import Blueprint,render_template
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
# Create a Blueprint
schedule_dashboard = Blueprint('schedule_dashboard', __name__)

# Define your routes using the Blueprint
@schedule_dashboard.route('/employer/schedule_dashboard')
@verify_user
@is_email_verified
def schedule_dashboard_():
    return render_template('/pages/recruiter/schedule-dashboard.html')