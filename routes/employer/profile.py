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
            (SELECT GROUP_CONCAT(CONCAT_WS('||||', job_id, title, posted_at, status) SEPARATOR ';;;;') FROM active_job_postings) AS active_job_postings,
            (SELECT email FROM contact_information) AS email,
            (SELECT website FROM contact_information) AS contact_website,
            (SELECT total_jobs_posted FROM job_statistics) AS total_jobs_posted,
            (SELECT currently_active_jobs FROM job_statistics) AS currently_active_jobs,
            (SELECT GROUP_CONCAT(CONCAT_WS('||||', status, count) SEPARATOR ';;;;') FROM chart_data) AS chart_data,
            (SELECT GROUP_CONCAT(CONCAT_WS('||||', first_name, last_name, position, status) SEPARATOR ';;;;') FROM recent_applications) AS recent_applications
    """)
    
    result = db.execute_query(query, {"employer_id": employer_id})
    
    if result["success"]:
       
        # Process active job postings data
        if not result["output"]: # Handle case where query returns no data for the employer_id
            # Return a structure with default/empty values if appropriate for your frontend
            return jsonify({
                'success': True,
                'data': [{
                    'total_candidates': 0,
                    'total_job_posted': 0,
                    'active_job_listings': 0,
                    'successful_hires': 0,
                    'company_name': None,
                    'field': None,
                    'logo_url': None,
                    'industry': None,
                    'company_size': None,
                    'company_website': None,
                    'active_job_postings': [],
                    'email': None,
                    'contact_website': None,
                    'currently_active_jobs': 0,
                    'chart_data': [],
                    'recent_applications': []
                }]
            })

        data_row = result["output"][0]

        active_postings_str = data_row.get('active_job_postings')
        processed_postings = []
        if active_postings_str:
            job_entries = active_postings_str.split(';;;;')
            for entry in job_entries:
                if not entry: continue
                parts = entry.split('||||')
                if len(parts) == 4:
                    processed_postings.append({
                        'job_id': parts[0],
                        'title': parts[1],
                        'posted_at': parts[2],
                        'status': parts[3]
                    })
                else:
                    print(f"Warning: Malformed active_job_posting entry: {entry}") # Add logging
        data_row['active_job_postings'] = processed_postings
               
        # Process chart data
        chart_data_str = data_row.get('chart_data')
        processed_chart_data = []
        if chart_data_str:
            chart_entries = chart_data_str.split(';;;;')
            for entry in chart_entries:
                if not entry: continue
                parts = entry.split('||||')
                if len(parts) == 2:
                    processed_chart_data.append({
                        'status': parts[0],
                        'count': int(parts[1]) if parts[1].isdigit() else parts[1]
                    })
                else:
                    print(f"Warning: Malformed chart_data entry: {entry}") # Add logging
        data_row['chart_data'] = processed_chart_data

        # Process recent applications data
        recent_apps_str = data_row.get('recent_applications')
        processed_recent_apps = []
        if recent_apps_str:
            app_entries = recent_apps_str.split(';;;;')
            for entry in app_entries:
                if not entry: continue
                parts = entry.split('||||')
                if len(parts) == 4:
                    processed_recent_apps.append({
                        'first_name': parts[0],
                        'last_name': parts[1],
                        'position': parts[2],
                        'status': parts[3]
                    })
                else:
                    print(f"Warning: Malformed recent_application entry: {entry}") # Add logging
        data_row['recent_applications'] = processed_recent_apps

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
