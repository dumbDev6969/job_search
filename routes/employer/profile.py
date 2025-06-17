from flask import Blueprint,render_template
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
from flask import request, jsonify
from utils.database import get_db
from sqlalchemy import text
from flask import session
from middlewares.is_requirements_done import is_requirements_done


# Create a Blueprint
profile = Blueprint('profile', __name__)

# Define your routes using the Blueprint
@profile.route('/employer/profile')
@verify_user
@is_email_verified
@is_requirements_done
def profile_():
    """
    Render the employer profile page.

    This route displays the profile page for employers where they can view their
    personal information and profile details. Access requires user authentication
    and email verification.

    Decorators:
        @verify_user: Ensures the user is authenticated
        @is_email_verified: Ensures the user's email is verified
        @is_requirements_done: Ensures the user has completed the requirements

    Returns:
        rendered template: The employer profile HTML page
    """
    return render_template('/pages/recruiter/profile.html',id = session.get('user_id'))



@profile.route('/api/employer/data/<int:id>', methods=['GET'])
@verify_user
@is_email_verified
@is_requirements_done
def get_active_job_postings(id):
    """
    Retrieve active job postings and related statistics for an employer.

    This function queries the database to gather various statistics and
    information about an employer's active job postings, including the number
    of total candidates, total jobs posted, active job listings, successful
    hires, and company profile details. Additionally, it fetches contact
    information, job statistics, chart data on application statuses, and
    recent applications.

    Parameters:
        id (int): The employer's ID to query data for.

    Returns:
        JSON response containing success status and the retrieved data if
        successful, otherwise a JSON response with an error message and
        HTTP status 500.
    """

    db = get_db()
    employer_id = id  # Using static user ID as requested
    
    query = text("""
        WITH dashboard_summary AS (
            SELECT COUNT(DISTINCT a.seeker_id) AS total_candidates
            FROM applications a
            JOIN jobs j ON a.job_id = j.job_id
            WHERE j.employer_id = :employer_id
        ),
        total_job_posted AS (
            SELECT COUNT(*) AS total_job_posted
            FROM jobs
            WHERE employer_id = :employer_id
        ),
        active_job_listings AS (
            SELECT COUNT(*) AS active_job_listings
            FROM jobs
            WHERE employer_id = :employer_id AND status = 'active'
        ),
        successful_hires AS (
            SELECT COUNT(*) AS successful_hires
            FROM applications a
            JOIN jobs j ON a.job_id = j.job_id
            WHERE j.employer_id = :employer_id AND a.status = 'shortlisted'
        ),
        company_profile AS (
            SELECT company_name, logo_url, industry, company_size, website, field
            FROM employers
            WHERE employer_id = :employer_id
        ),
        active_job_postings AS (
            SELECT job_id, title, posted_at, status
            FROM jobs
            WHERE employer_id = :employer_id AND status = 'active'
            ORDER BY posted_at DESC
        ),
        contact_information AS (
            SELECT email, website
            FROM employers
            WHERE employer_id = :employer_id
        ),
        job_statistics AS (
            SELECT 
                (SELECT COUNT(*) FROM jobs WHERE employer_id = :employer_id) AS total_jobs_posted,
                (SELECT COUNT(*) FROM jobs WHERE employer_id = :employer_id AND status = 'active') AS currently_active_jobs
        ),
        chart_data AS (
            SELECT a.status, COUNT(*) AS count
            FROM applications a
            JOIN jobs j ON a.job_id = j.job_id
            WHERE j.employer_id = :employer_id
            GROUP BY a.status
        ),
        recent_applications AS (
            SELECT js.first_name, js.last_name, j.title AS position, a.status
            FROM applications a
            JOIN jobs j ON a.job_id = j.job_id
            JOIN job_seekers js ON a.seeker_id = js.seeker_id
            WHERE j.employer_id = :employer_id
            ORDER BY a.applied_at DESC
            LIMIT 10
        )
        SELECT 
            (SELECT total_candidates FROM dashboard_summary) AS total_candidates,
            (SELECT total_job_posted FROM total_job_posted) AS total_job_posted,
            (SELECT active_job_listings FROM active_job_listings) AS active_job_listings,
            (SELECT successful_hires FROM successful_hires) AS successful_hires,
            (SELECT company_name FROM company_profile) AS company_name,
            (SELECT field FROM company_profile) AS field,
            (SELECT logo_url FROM company_profile) AS logo_url,
            (SELECT industry FROM company_profile) AS industry,
            (SELECT company_size FROM company_profile) AS company_size,
            (SELECT website FROM company_profile) AS company_website,
            (SELECT GROUP_CONCAT(CONCAT_WS('|', job_id, title, posted_at, status)) FROM active_job_postings) AS active_job_postings,
            (SELECT email FROM contact_information) AS email,
            (SELECT website FROM contact_information) AS contact_website,
            (SELECT total_jobs_posted FROM job_statistics) AS total_jobs_posted,
            (SELECT currently_active_jobs FROM job_statistics) AS currently_active_jobs,
            (SELECT GROUP_CONCAT(CONCAT_WS('|', status, count)) FROM chart_data) AS chart_data,
            (SELECT GROUP_CONCAT(CONCAT_WS('|', first_name, last_name, position, status)) FROM recent_applications) AS recent_applications
    """)
    
    result = db.execute_query(query, {"employer_id": employer_id})
    
    if result["success"]:
       
        # Process active job postings data
        if result["output"][0]['active_job_postings']:
            splitted =result["output"][0]['active_job_postings'].split('|')
            result["output"][0]['active_job_postings'] = []
            result["output"][0]['active_job_postings'].append(
                {
                    'job_id': splitted[0],
                    'title': splitted[1],
                    'posted_at': splitted[2],
                    'status': splitted[3]
                }
            )
               
        # Process chart data
        if result["output"][0]['chart_data']:
            result["output"][0]['chart_data'] = result["output"][0]['chart_data'].split('|')
        
        # Process recent applications data
        if result["output"][0]['recent_applications']:
            result["output"][0]['recent_applications'] = result["output"][0]['recent_applications'].split('|')

        print(result["output"])
        return jsonify({
            'success': True,
            'data': result["output"]
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch active job postings'
        }), 500
