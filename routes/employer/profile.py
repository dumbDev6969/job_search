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