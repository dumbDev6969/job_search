from flask import Blueprint, render_template
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified


# Create a Blueprint
requirements = Blueprint("requirements", __name__)


# Define your routes using the Blueprint
@requirements.route("/employer/requirements")
@verify_user
@is_email_verified
def requirements_():
    return render_template("/pages/recruiter/requirement.html")
