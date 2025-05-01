from flask import Blueprint,render_template,jsonify,request,redirect,session
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
from middlewares.is_setup_done import is_interests_done,is_qualification_done
from middlewares.user_access import jobseeker as job_seeker_middleware,admin,emplyer
from utils.database import get_db
from sqlalchemy import text

# Create a Blueprint
apply_job = Blueprint('apply_job', __name__)



@apply_job.route('/api/jobseeker/apply', methods=['POST'])
@verify_user
def apply():
    job_id=request.form.get('job_id')
    seeker_id =  session['user_id']
    resume_url =''
    cover_letter = ''
    status = 'applied'
    db = get_db()

    sql = f"""INSERT INTO `applications`
(`application_id`, `job_id`, `seeker_id`, `resume_url`, `cover_letter`, `status`, `applied_at`)
VALUES (
    NULL,
    {job_id},
    {seeker_id},
    '{resume_url}',
    '{cover_letter}',
    '{status}',
    current_timestamp()
)"""

    results = db.execute_query(text(sql))

    if results['success']:
        return results
    else:
        return results