from flask import Blueprint, render_template
from middlewares.verify_user import verify_user

recruiter_approval = Blueprint('recruiter_approval', __name__)

@recruiter_approval.route('/admin/recruiter_approval')
@recruiter_approval.route('/admin/recruiter_approval.html')
@verify_user
def recruiter_approval_view():
    return render_template('/pages/admin/recruiter_approval.html')