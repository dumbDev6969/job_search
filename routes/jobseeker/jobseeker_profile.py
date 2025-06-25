

from flask import Blueprint, render_template, session , request, jsonify
from sqlalchemy import text

from middlewares.is_email_verified import is_email_verified
from middlewares.is_setup_done import is_interests_done, is_qualification_done
from middlewares.skills_and_resume import is_skills_and_resume_done
from middlewares.user_access import jobseeker as jobseeker
from middlewares.verify_user import verify_user
from utils.check_if_exists import check_column_exists

# Create a Blueprint
jobseeker_profile = Blueprint("jobseeker_profile", __name__)


# Define your routes using the Blueprint
@jobseeker_profile.route("/jobseeker/profile")
@verify_user
@is_email_verified
@is_interests_done
@is_qualification_done
@is_skills_and_resume_done
def jobseeker_profile_():
    """Render the job seeker's profile page.

    This route displays the profile page for job seekers where they can view their
    personal information and profile details. Access requires user authentication
    and email verification.

    Decorators:
        @verify_user: Ensures the user is authenticated
        @is_email_verified: Ensures the user's email is verified

    Returns:
        rendered template: The job seeker profile HTML page
    """
    logging.info("Rendering job seeker profile page")
    return render_template("/pages/job_seeker/profile.html")


@jobseeker_profile.route("/jobseeker/profile-setting")
@verify_user
@is_email_verified
@is_interests_done
@is_qualification_done
@is_skills_and_resume_done
def jobseeker_profile_settings():
    """Render the job seeker's profile settings page.

    This route displays the settings page where job seekers can modify their
    profile information and preferences. Access requires user authentication
    and email verification.

    Decorators:
        @verify_user: Ensures the user is authenticated
        @is_email_verified: Ensures the user's email is verified

    Returns:
        rendered template: The job seeker profile settings HTML page
    """
    logging.info("Rendering job seeker profile settings page")
    return render_template("/pages/job_seeker/profile_settings.html")


import json

from utils.database import get_db


@jobseeker_profile.route("/jobseeker/profile-data")
@verify_user
@is_email_verified
def jobseeker_profile_data():
    """
    API endpoint to fetch job seeker profile data.
    """
    logging.info("Fetching job seeker profile data")
    try:
        db = get_db()
        email = session.get("email")

        # Fetch job seeker data from the database
        sql = text(f"""
            SELECT
                js.first_name,
                js.last_name,
                js.email,
                js.phone,
                js.province,
                js.municipality,
                js.degree,
                js.portfolio_url,
                q.school_graduated,
                q.certifications,
                q.specialized_training,
                ji.job_interest,
                ji.job_type,
                ji.preferred_location,
                ji.expected_salary_range
            FROM job_seekers js
            LEFT JOIN qualifications q ON js.seeker_id = q.seeker_id
            LEFT JOIN job_interest ji ON js.seeker_id = ji.user_id
            WHERE js.email = '{email}'
        """)
        result = db.execute_query(sql)

        if result["success"]:
            logging.info("Job seeker profile data fetched successfully")
            return json.dumps(result["output"])
        else:
            logging.error("Profile not found")
            return json.dumps({"message": "Profile not found"}), 404

    except Exception as e:
        logging.error(f"Error fetching profile data: {e}")
        return json.dumps({"message": "Error fetching profile data"}), 500


@jobseeker_profile.route("/view-profile/jobseeker/<int:seeker_id>")
@is_email_verified
def jobseeker_details(seeker_id):
    """
    Render the job seeker's details page with dynamic data.
    """
    logging.info(f"Fetching job seeker details for seeker_id {seeker_id}")
    if not check_column_exists("job_seekers", "seeker_id ", seeker_id):
        logging.warning(f"Job seeker with id {seeker_id} not found")
        return render_template("/pages/user_not_found.html")
    db = get_db()

    sql = text("""
        SELECT
            js.seeker_id,
            js.first_name,
            js.last_name,
            js.email,
            js.phone,
            js.province,
            js.municipality,
            js.degree,
            js.portfolio_url,
            q.school_graduated,
            q.certifications,
            q.specialized_training,
            ji.job_interest,
            ji.job_type,
            ji.preferred_location,
            ji.expected_salary_range,
            js.*,
            q.*,
               ji.*
        FROM job_seekers js
        LEFT JOIN qualifications q ON js.seeker_id = q.seeker_id
        LEFT JOIN job_interest ji ON js.seeker_id = ji.user_id
        WHERE js.seeker_id = :seeker_id
    """)
    result = db.execute_query(sql, {"seeker_id": seeker_id})

    if not result["success"] or not result["output"]:
        logging.error("Error fetching job seeker details:", result)
        return render_template(
            "/pages/job_seeker/seeker_detals.html", error="Job seeker not found."
        )
    seeker = result["output"][0]
    logging.info(f"Job seeker details for seeker_id {seeker_id} fetched successfully")
    return render_template(
        "/pages/job_seeker/seeker_detals.html", seeker=result["output"][0]
    )


@jobseeker_profile.route('/jobseeker/profile-update', methods=['POST'])
@verify_user
@is_email_verified
def update_jobseeker_profile():
    """
    Update a job seeker's profile.

    This API endpoint receives a JSON payload containing the updated profile
    information and updates the corresponding fields in the database.
    """
    logging.info("Updating job seeker profile for user: %s", session.get('user_id'))
    data = request.get_json()
    db = get_db()
    seeker_id = session.get('user_id')
    if seeker_id is None:
        logging.error("User not logged in.")
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
        logging.info("Profile updated successfully for user: %s", session.get('user_id'))
        return jsonify({'success': True, 'message': 'Profile updated!'})
    else:
        logging.error("Failed to update profile for user: %s", session.get('user_id'))
        return jsonify({'success': False, 'message': 'Failed to update profile.'}), 500
