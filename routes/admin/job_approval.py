from flask import Blueprint, render_template
from middlewares.verify_user import verify_user

job_approval = Blueprint('job_approval', __name__)

@job_approval.route('/admin/job_approval')
@job_approval.route('/admin/job_approval.html')
@verify_user
def job_approval_view():
    return render_template('/pages/admin/job_approval.html')