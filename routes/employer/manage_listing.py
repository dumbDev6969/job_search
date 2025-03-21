from flask import Blueprint,render_template
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
# Create a Blueprint
manage_listing = Blueprint('manage_listing', __name__)

# Define your routes using the Blueprint
@manage_listing.route('/employer/manage_listing')
@verify_user
@is_email_verified
def manage_listing_():
    return render_template('/pages/recruiter/manage_listing.html')
