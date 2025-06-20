

from flask import Blueprint, render_template, session, jsonify
import logging
from middlewares.is_email_verified import is_email_verified
from middlewares.user_access import jobseeker as jobseeker, admin, emplyer
from middlewares.is_setup_done import is_interests_done, is_qualification_done
from utils.database import get_db
from sqlalchemy import text
from middlewares.verify_user import verify_user



# Create a Blueprint
recomendations = Blueprint("recomendations", __name__)


# Define your routes using the Blueprint
@recomendations.route("/jobseeker/recomendations")
@verify_user
@is_email_verified
@is_interests_done
@is_qualification_done
def recomendations_():
    """
    Fetches recommended jobs and renders the recommendation page with the job listings.
    """
    logging.info("Rendering job recommendations page.")
    jobs = get_recommended_jobs()
    return render_template("/pages/job_seeker/recommendation.html", jobs=jobs)


@recomendations.route("/jobseeker/get-recomendations")
@verify_user
@is_email_verified
@is_interests_done
@is_qualification_done
def get_recommended_jobs():
    """
    Retrieves a list of recommended job opportunities for a job seeker.

    The function queries the database for job recommendations based on the job seeker's
    skills and interests. It is decorated with various middlewares to ensure the user
    is authenticated, their email is verified, and their profile setup is complete,
    including interests and qualifications.

    Returns:
        list: A list of dictionaries where each dictionary represents a job with
        keys 'title', 'location', 'salary_range', and 'employer'.
    """
    db = get_db()
    logging.info("Attempting to fetch recommended jobs.")
    job_seeker_id = session.get("user_id")
    logging.info("Fetching job recommendations for job seeker ID: %s", job_seeker_id)

    # Query the database for the job seeker's interests
    query = text("""
        SELECT job_interest, job_type, preferred_location, expected_salary_range
        FROM job_interest
        WHERE user_id = :job_seeker_id
    """)
    params = {"job_seeker_id": job_seeker_id}
    job_seeker_interests = db.execute_query(query, params=params)
    logging.debug("Job seeker interests fetched: %s", job_seeker_interests)

    if not job_seeker_interests["output"]:
        logging.warning("No job seeker interests found for ID: %s", job_seeker_id)
        return jsonify({"success": False, "jobs": [], "message": "No job interests found for this user."}), 200

    job_seeker_interests = job_seeker_interests["output"][0]
    logging.info("Processed job seeker interests: %s", job_seeker_interests)

    # Extract job seeker's preferences
    job_seeker_interest = job_seeker_interests["job_interest"].lower()
    job_seeker_job_type = job_seeker_interests["job_type"].lower()
    job_seeker_location = job_seeker_interests["preferred_location"].lower()
    job_seeker_salary_range = job_seeker_interests["expected_salary_range"]
    logging.info("Job seeker preferences extracted: interest=%s, type=%s, location=%s, salary=%s",
 job_seeker_interest, job_seeker_job_type, job_seeker_location, job_seeker_salary_range)

    # Query the database for jobs that match the job seeker's skills and job type
    query = text("""
        SELECT j.job_id AS id, j.title, j.location, j.salary_range, e.company_name AS employer
        FROM jobs j
        JOIN employers e ON j.employer_id = e.employer_id
        WHERE 
            (j.employment_type LIKE :job_seeker_job_type OR 
            j.location = :job_seeker_location OR 
            j.salary_range = :job_seeker_salary_range) AND j.approved = 1 AND j.status = 'active'
    """)
    params = {
        "job_seeker_interest": job_seeker_interest,
        "job_seeker_job_type": job_seeker_job_type,
        "job_seeker_location": job_seeker_location,
        "job_seeker_salary_range": job_seeker_salary_range
    }
    jobs = db.execute_query(query, params=params)
    logging.debug("Jobs fetched from database: %s", jobs)

    if not jobs["output"]:
        logging.warning("No matching jobs found for preferences: %s", params)
        return jsonify({"success": False, "empty": True, "jobs": "<div class='col-12 text-center py-5'><h4>No jobs found matching your criteria</h4><p>Try adjusting your search filters</p></div>", "message": "No matching jobs found."}), 200

    # Format the jobs data
    recommended_jobs = []

    for job in jobs["output"]:
        recommended_job = {
            "id": job["id"],
            "title": job["title"],
            "location": job["location"],
            "salary_range": job["salary_range"],
            "employer": job["employer"],
        }
        logging.debug("Recommended job added: %s", recommended_job)
        recommended_jobs.append(recommended_job)

    logging.info("Total recommended jobs: %d", len(recommended_jobs))
    return jsonify({"success": True, "jobs": recommended_jobs}), 200
