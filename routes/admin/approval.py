from flask import Blueprint,render_template
from middlewares.verify_user import verify_user

# Create a Blueprint
approval = Blueprint('approval', __name__)

# Define your routes using the Blueprint=
@approval.route('/admin/approval')
@verify_user
def job_approval():
    pass

@approval.route('/admin/approval')
@verify_user
def recruiter_approval():
    pass

