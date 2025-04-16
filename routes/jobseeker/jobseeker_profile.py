from flask import Blueprint,render_template,session
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
from middlewares.user_access import jobseeker as jobseeker,admin,emplyer
from middlewares.is_setup_done import is_interests_done,is_qualification_done
from sqlalchemy import text


# Create a Blueprint
jobseeker_profile= Blueprint('jobseeker_profile', __name__)

# Define your routes using the Blueprint
@jobseeker_profile.route('/jobseeker/profile')
@verify_user
@is_email_verified
@is_interests_done
@is_qualification_done
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
    return render_template('/pages/job_seeker/profile.html')


@jobseeker_profile.route('/jobseeker/profile-setting')
@verify_user
@is_email_verified
@is_interests_done
@is_qualification_done
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
    return render_template('/pages/job_seeker/profile_settings.html')

from utils.database import get_db
import json

@jobseeker_profile.route('/jobseeker/profile-data')
@verify_user
@is_email_verified
def jobseeker_profile_data():
    """
    API endpoint to fetch job seeker profile data.
    """
   
    try:
        db = get_db()
        email = session.get('email')
       
        # Fetch job seeker data from the database
        sql  = text(f"""
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

      

        if result['success']:
            return json.dumps(result['output'])
        else:
            return json.dumps({'message': 'Profile not found'}), 404

    except Exception as e:
        print(f"Error fetching profile data: {e}")
        return json.dumps({'message': 'Error fetching profile data'}), 500
   