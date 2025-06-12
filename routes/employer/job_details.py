

from flask import Blueprint,render_template
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
from middlewares.is_requirements_done import is_requirements_done
from utils.database import get_db
from sqlalchemy import text

# Create a Blueprint
job_details = Blueprint('job_details', __name__)

# Define your routes using the Blueprint
@job_details.route('/employer/job/<int:job_id>')
@verify_user
@is_email_verified
@is_requirements_done
def job_details_(job_id):
    db = get_db()
    result = db.execute_query(text(f"SELECT * FROM jobs WHERE job_id = {job_id}"))
    if result["success"]:
        if  result["output"]:
            employer_details =  db.execute_query(text(f"SELECT * FROM employers WHERE employer_id = {result['output'][0]['employer_id']}"))
            if employer_details["success"]:
                result["output"][0]["employer_details"] = employer_details["output"][0]
            return render_template('/pages/recruiter/job_details.html', job=result["output"][0])
    return render_template('/pages/recruiter/job_details.html')