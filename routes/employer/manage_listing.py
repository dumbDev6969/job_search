from flask import Blueprint, render_template, request, session
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
from utils.database import get_db
from sqlalchemy import text
from middlewares.is_requirements_done import is_requirements_done
import logging


# Create a Blueprint
manage_listing = Blueprint('manage_listing', __name__)


# Define your routes using the Blueprint
@manage_listing.route('/employer/manage_listing')
@verify_user
@is_email_verified
@is_requirements_done
def manage_listing_():
    return render_template('/pages/recruiter/manage_listing.html')




@manage_listing.route('/employer/api/get_listing', methods=['GET', 'POST'])
@verify_user
@is_email_verified
@is_requirements_done
def get_listing_api():
    """
    Returns a list of job applications filtered by search, salary, location, and skills.

    GET Parameters:
        search (str): Search for job applications by name, skills, job title, or job description.
        salary (str): Filter job applications by salary range.
        location (str): Filter job applications by job location.
        skills (str): Filter job applications by job seeker skills.

    Returns:
        dict: A dictionary containing the HTML content of the job applications table and the total number of job applications.
    """
    db = get_db()
    search = request.args.get('search', '')
    salary = request.args.get('salary', '')
    location = request.args.get('location', '')
    skills = request.args.get('skills', '')

    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10)) # Default to 10 items per page
    offset = (page - 1) * per_page

    employer_id = session.get('user_id')
    logging.info(f"Requested job listing with search: {search}, salary: {salary},"
                 f" location: {location}, skills: {skills}, page: {page}, per_page: {per_page}")

    base_query_cte = """
    WITH filtered_applications AS (
        SELECT
            a.application_id,
            a.status as application_status,
            a.applied_at,
            a.resume_url,
            a.cover_letter,
            j.title as job_title,
            j.description as job_description,
            ji.preferred_location as job_location,
            j.salary_range,
            j.employment_type,
            CONCAT(js.first_name, ' ', js.last_name) as applicant_name,
            js.email as applicant_email,
            js.phone as applicant_phone,
            js.province as applicant_province,
            q.specialized_training as skills
        FROM applications a
        JOIN jobs j ON a.job_id = j.job_id
        JOIN job_seekers js ON a.seeker_id = js.seeker_id
        LEFT JOIN qualifications q ON js.seeker_id = q.seeker_id
        LEFT JOIN job_interest ji ON js.seeker_id = ji.user_id
        WHERE j.employer_id = :employer_id
    """

    count_query_sql = base_query_cte + ") SELECT COUNT(DISTINCT application_id) as total FROM filtered_applications"
    main_query_sql = base_query_cte + ") SELECT * FROM filtered_applications"

    params = {'employer_id': employer_id}
    conditions = []

    if search or salary or location or skills:
        if search:
            conditions.append(f"(LOWER(applicant_name) LIKE LOWER(:search_term) OR LOWER(skills) LIKE LOWER(:search_term))")
            params['search_term'] = f'%{search}%'

        if salary:
            conditions.append(f"salary_range LIKE :salary_term")
            params['salary_term'] = f'%{salary}%'

        if location:
            conditions.append(f"job_location LIKE :location_term")
            params['location_term'] = f'%{location}%'

        if skills:
            conditions.append(f"skills LIKE :skills_term")
            params['skills_term'] = f'%{skills}%'

    if conditions:
        filter_clause = " WHERE " + " AND ".join(conditions)
        count_query_sql += filter_clause
        main_query_sql += filter_clause

    # Execute count query first
    logging.info(f"Constructed count query: {count_query_sql}")
    logging.info(f"Count query params: {params}")
    count_result = db.execute_query(text(count_query_sql), params)
    total_candidates = 0
    if count_result['success'] and count_result['output']:
        total_candidates = count_result['output'][0]['total']
    else:
        logging.error(f"Count query failed: {count_result.get('error', 'Unknown error')}")

    total_pages = (total_candidates + per_page - 1) // per_page

    # Add ordering and pagination to the main query
    main_query_sql += " ORDER BY applied_at DESC LIMIT :limit OFFSET :offset"
    params['limit'] = per_page
    params['offset'] = offset

    logging.info(f"Constructed main query: {main_query_sql}")
    logging.info(f"Main query params: {params}")

    result = db.execute_query(text(main_query_sql), params)

    html_content = ""
    if result['success'] and result['output']:
        jobs = result['output']
        # total_candidates is already set from the count query
        logging.info(f"Found {total_candidates} job applications")
        for job in jobs:
            html_content += f"""<tr>
                <td><input type="checkbox" class="form-check-input"></td>
                <td>
                    <div class="d-flex align-items-center">
                        <img src="https://randomuser.me/api/portraits/men/1.jpg" 
                             class="rounded-circle me-2" width="36" height="36">
                        <div>
                            <div class="fw-bold">{job['applicant_name']}</div>
                            <small class="text-muted">{job.get('job_title', 'N/A')}</small> 
                        </div>
                    </div>
                </td>
                <td><span class="badge bg-success">Available</span></td>
                <td>
                    <span class="badge bg-light text-dark me-1">{job['skills']}</span>
                </td>
                <td>{job['salary_range']}</td>
                <td>{job['job_location'] or 'N/A'}</td>
                <td>
                    <button class="btn btn-sm btn-outline-primary">
                        <i class="fas fa-eye"></i>
                    </button>
                </td>
            </tr>"""
        logging.info("Fetched job applications successfully")
        
        return {
            'html': html_content,
            'total': total_candidates,
            'total_pages': total_pages,
            'current_page': page
        }
    else:
        logging.info("No job applications found")
        return {'html': """
            <tr>
                <td colspan="7" class="text-center py-4">
                    <div class="d-flex flex-column align-items-center">
                        <i class="fas fa-search fa-3x text-muted mb-3"></i>
                        <h5 class="text-muted">No listings found</h5>
                        <p class="text-muted">There are currently no job applications to display.</p>
                    </div>
                </td>
            </tr>
        """,
        'total': 0,
        'total_pages': 0,
        'current_page': 1
        }


@manage_listing.route('/employer/api/dashboard_data')
@verify_user
@is_email_verified
@is_requirements_done
def get_dashboard_data():
    db = get_db()
    employer_id = session.get('user_id')  # or however you retrieve the current employer's ID

    # Total Candidates (for this employer)
    total_candidates_query = text("""
        SELECT COUNT(a.application_id) 
        FROM applications a
        INNER JOIN jobs j ON a.job_id = j.job_id
        WHERE j.employer_id = :employer_id
    """)
    total_candidates_result = db.execute_query(total_candidates_query, {'employer_id': employer_id})
    if total_candidates_result['success'] and total_candidates_result['output']:
        total_candidates = total_candidates_result['output'][0]['COUNT(a.application_id)']
    else:
        total_candidates = 0
        logging.info("Failed to retrieve total candidates")

    # Total Job Posted (by this employer)
    total_jobs_query = text("""
        SELECT COUNT(job_id) 
        FROM jobs 
        WHERE employer_id = :employer_id
    """)
    total_jobs_result = db.execute_query(total_jobs_query, {'employer_id': employer_id})
    if total_jobs_result['success'] and total_jobs_result['output']:
        total_job_posted = total_jobs_result['output'][0]['COUNT(job_id)']
    else:
        total_job_posted = 0
        logging.info("Failed to retrieve total jobs posted")

    # Active Job Listings (by this employer)
    active_jobs_query = text("""
        SELECT COUNT(job_id) 
        FROM jobs 
        WHERE employer_id = :employer_id AND expires_at > NOW() AND status = 'active'
    """)
    active_jobs_result = db.execute_query(active_jobs_query, {'employer_id': employer_id})
    if active_jobs_result['success'] and active_jobs_result['output']:
        active_job_listings = active_jobs_result['output'][0]['COUNT(job_id)']
    else:
        active_job_listings = 0
        logging.info("Failed to retrieve active job listings")

    # Successful Hires (applications with status 'reviewed' or 'shortlisted' for this employer)
    successful_hires_query = text("""
        SELECT COUNT(a.application_id) 
        FROM applications a
        INNER JOIN jobs j ON a.job_id = j.job_id
        WHERE j.employer_id = :employer_id AND a.status IN ('reviewed', 'shortlisted')
    """)
    successful_hires_result = db.execute_query(successful_hires_query, {'employer_id': employer_id})
    if successful_hires_result['success'] and successful_hires_result['output']:
        successful_hires = successful_hires_result['output'][0]['COUNT(a.application_id)']
    else:
        successful_hires = 0
        logging.info("Failed to retrieve successful hires")

    return {
        'total_candidates': total_candidates,
        'total_job_posted': total_job_posted,
        'active_job_listings': active_job_listings,
        'successful_hires': successful_hires
    }

@manage_listing.route('/employer/api/dashboard_tables')
@verify_user
@is_email_verified
def get_dashboard_tables():
    db = get_db()
    logger = logging.getLogger('flask_app')

    # Candidates Table Data
    candidates_query = text("""
        SELECT
            a.application_id,
            CONCAT(js.first_name, ' ', js.last_name) as applicant_name,
            j.title as job_title,
            a.status as application_status
        FROM applications a
        JOIN jobs j ON a.job_id = j.job_id
        JOIN job_seekers js ON a.seeker_id = js.seeker_id
        ORDER BY a.applied_at DESC
    """)
    candidates_result = db.execute_query(candidates_query)
    if candidates_result['success']:
        candidates_data = candidates_result['output']
    else:
        logger.info("Failed to retrieve candidates data")
        candidates_data = []

    # Recent Applications Data
    recent_applications_query = text("""
        SELECT
            a.application_id,
            CONCAT(js.first_name, ' ', js.last_name) as applicant_name,
            j.title as job_title,
            a.status as application_status
        FROM applications a
        JOIN jobs j ON a.job_id = j.job_id
        JOIN job_seekers js ON a.seeker_id = js.seeker_id
        ORDER BY a.applied_at DESC
        LIMIT 5
    """)
    recent_applications_result = db.execute_query(recent_applications_query)
    if recent_applications_result['success']:
        recent_applications_data = recent_applications_result['output']
    else:
        logger.info("Failed to retrieve recent applications data")
        recent_applications_data = []

    # Upcoming Interviews Data
    upcoming_interviews_query = text("""
        SELECT
            i.interview_id,
            CONCAT(js.first_name, ' ', js.last_name) as applicant_name,
            j.title as job_title,
            a.applied_at,
            i.status as interview_status
        FROM interviews i
        JOIN applications a ON i.seeker_id = a.seeker_id
        JOIN jobs j ON a.job_id = j.job_id
        JOIN job_seekers js ON i.seeker_id = js.seeker_id
        ORDER BY a.applied_at DESC
        LIMIT 5
    """)
    upcoming_interviews_result = db.execute_query(upcoming_interviews_query)
    if upcoming_interviews_result['success']:
        upcoming_interviews_data = upcoming_interviews_result['output']
    else:
        logger.info("Failed to retrieve upcoming interviews data")
        upcoming_interviews_data = []

    return {
        'candidates': candidates_data,
        'recent_applications': recent_applications_data,
        'upcoming_interviews': upcoming_interviews_data
    }
