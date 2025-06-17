from flask import Blueprint,render_template, session
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
    """
    This function renders the job details page when an employer
    is logged in and the employer_id matches the one in the jobs table.
    The employer's details are also retrieved from the employers table
    and added to the response.
    Parameters:
        job_id (int): The id of the job to display.
    Returns:
        A rendered template of the job details page.
    """
    db = get_db()
    result = db.execute_query(text(f"SELECT * FROM jobs WHERE job_id = {job_id}"))
    if result["success"]:
        if  result["output"]:
            logging.info(f"Fetching job details for job id {job_id}")
            employer_details =  db.execute_query(text(f"SELECT * FROM employers WHERE employer_id = {result['output'][0]['employer_id']}"))
            if employer_details["success"]:
                logging.info(f"Fetching employer details for job id {job_id}")
                result["output"][0]["employer_details"] = employer_details["output"][0]
                is_job_seeker = True if session.get('user_type') == 'seeker' else False
            return render_template('/pages/recruiter/job_details.html', job=result["output"][0], is_job_seeker=is_job_seeker, back=['/employer/jobs','jobs'])
        else:
            logging.error(f"Job id {job_id} not found")
    return render_template('/pages/recruiter/job_details.html')

@job_details.route('/job/view/<int:job_id>')
def job_details_public(job_id):
    """ 
    This function renders the job details page when the user navigates to /job/view/<int:job_id>
    It fetches the job details from the jobs table and the employer details from the employers table
    and renders the job_details.html template with the job and employer details
    If the job or employer details are not found, it renders the job_details.html template with an error message
    """
    db = get_db()
    result = db.execute_query(text(f"SELECT * FROM jobs WHERE job_id = {job_id}"))
    
    if result["success"]:
        if result["output"]:
            logging.info(f"Fetching job details for job id {job_id}")
            employer_details = db.execute_query(text(f"SELECT * FROM employers WHERE employer_id = {result['output'][0]['employer_id']}"))
            
            if employer_details["success"]:
                logging.info(f"Fetching employer details for employer id {result['output'][0]['employer_id']}")
                result["output"][0]["employer_details"] = employer_details["output"][0]
                is_job_seeker = True if session.get('user_type') == 'seeker' else False
                  
                return render_template('/pages/recruiter/job_details.html', job=result["output"][0], is_job_seeker=is_job_seeker,back=['/jobseeker/recomendations','recomendations'])
            else:
                logging.error(f"Failed to fetch employer details for employer id {result['output'][0]['employer_id']}")
        else:
            logging.error(f"Job id {job_id} not found")
    else:
        logging.error(f"Failed to fetch job details for job id {job_id}")
    
    return render_template('/pages/recruiter/job_details.html', error="Job or Employer not found")
