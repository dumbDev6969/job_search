from flask import Blueprint,render_template
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
from flask import request, jsonify
from utils.database import get_db
from sqlalchemy import text
from flask import session

# Create a Blueprint
profile = Blueprint('profile', __name__)

# Define your routes using the Blueprint
@profile.route('/employer/profile')
@verify_user
@is_email_verified
def profile_():
    return render_template('/pages/recruiter/profile.html')

from flask import g

@profile.route('/jobseeker/profile-update', methods=['POST'])
@verify_user
@is_email_verified
def update_jobseeker_profile():
    data = request.get_json()
    db = get_db()
    seeker_id = session.get('user_id')
    if seeker_id is None:
        return jsonify({'success': False, 'message': 'User not logged in.'}), 401

    # Update qualifications
    qual_query = text("""
        UPDATE qualifications
        SET degree = :degree,
            school_graduated = :school_graduated,
            certifications = :certifications,
            specialized_training = :specialized_training
        WHERE seeker_id = :seeker_id
    """)
    qual_params = {
        "seeker_id": seeker_id,
        "degree": data.get("degree", ""),
        "school_graduated": data.get("school_graduated", ""),
        "certifications": data.get("certifications", ""),
        "specialized_training": data.get("specialized_training", "")
    }
    qual_result = db.execute_query(qual_query, qual_params)

    # Update job interest
    interest_query = text("""
        UPDATE job_interest
        SET job_interest = :job_interest,
            job_type = :job_type,
            preferred_location = :preferred_location,
            expected_salary_range = :expected_salary_range
        WHERE user_id = :user_id
    """)
    interest_params = {
        "user_id": seeker_id,
        "job_interest": data.get("job_interest", ""),
        "job_type": data.get("job_type", ""),
        "preferred_location": data.get("preferred_location", ""),
        "expected_salary_range": data.get("expected_salary_range", "")
    }
    interest_result = db.execute_query(interest_query, interest_params)

    if qual_result["success"] and interest_result["success"]:
        return jsonify({'success': True, 'message': 'Profile updated!'})
    else:
        return jsonify({'success': False, 'message': 'Failed to update profile.'}), 500


@profile.route('/api/employer/data', methods=['GET'])
@verify_user
@is_email_verified
def get_active_job_postings():
    db = get_db()
    employer_id = 3  # Using static user ID as requested
    
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
            SELECT company_name, logo_url, industry, company_size, website
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
            result["output"][0]['active_job_postings'] = result["output"][0]['active_job_postings'].split('|')
        
        # Process chart data
        if result["output"][0]['chart_data']:
            result["output"][0]['chart_data'] = result["output"][0]['chart_data'].split('|')
        
        # Process recent applications data
        if result["output"][0]['recent_applications']:
            result["output"][0]['recent_applications'] = result["output"][0]['recent_applications'].split('|')
        return jsonify({
            'success': True,
            'data': result["output"]
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch active job postings'
        }), 500
