

from flask import Blueprint,render_template
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
from middlewares.is_requirements_done import is_requirements_done

# Create a Blueprint
edit_job = Blueprint('edit_job', __name__)

# Define your routes using the Blueprint
@edit_job.route('/employer/edit_job')
@verify_user
@is_email_verified
@is_requirements_done
def edit_job_():
    return render_template('/pages/recruiter/edit-job..html')