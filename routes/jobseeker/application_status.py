from flask import Blueprint, render_template, session, jsonify
from middlewares.verify_user import verify_user
from utils.database import get_db
from sqlalchemy import text

# Create a Blueprint
application_status = Blueprint('application_status', __name__)

@application_status.route('/jobseeker/application-status', methods=['GET'])
@verify_user
def view_application_status():
    user_id = session['user_id']
    db = get_db()
    # Query to fetch application status along with job and company details
    sql = text("""
    SELECT 
        a.application_id, 
        a.job_id, 
        a.status, 
        a.applied_at, 
        j.title AS job_title, 
        e.company_name
    FROM 
        applications a
    JOIN 
        jobs j ON a.job_id = j.job_id
    JOIN 
        employers e ON j.employer_id = e.employer_id
    WHERE 
        a.seeker_id = :seeker_id
    ORDER BY 
        a.applied_at DESC;
    """)
    
    results = db.execute_query(sql, {'seeker_id': user_id})

    if results['success'] and results['output']:
        return render_template('pages/job_seeker/application_status.html', applications=results['output'])
    else:
        return render_template('pages/job_seeker/application_status.html', applications=[])
