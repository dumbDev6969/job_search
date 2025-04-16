from flask import Blueprint,render_template
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
from middlewares.user_access import jobseeker as jobseeker,admin,emplyer
from middlewares.is_setup_done import is_interests_done,is_qualification_done

# Create a Blueprint
jobseeker_skills_and_resume= Blueprint('jobseeker_skills_and_resume', __name__)

# Define your routes using the Blueprint
@jobseeker_skills_and_resume.route('/jobseeker/skills-and-resume')
@verify_user
@is_email_verified
@is_interests_done
@is_qualification_done
def jobseeker_skills_and_resume_():
    return render_template('/pages/job_seeker/skills_resume.html')



# from utils.database import get_db
# import json

# @jobseeker_profile.route('/jobseeker/profile-data')
# @verify_user
# @is_email_verified
# def jobseeker_profile_data():
#     """
#     API endpoint to fetch job seeker profile data.
#     """
#     conn = None  # Initialize conn to None
#     try:
#         db = get_db()
#         conn = db.engine.connect()
#         cursor = conn.cursor()

#         # Assuming you have user's email from the session
#         email = "jemcarlo46@gmail.com"  # Replace with actual session data

#         # Fetch job seeker data from the database
#         cursor.execute("""
#             SELECT
#                 js.first_name,
#                 js.last_name,
#                 js.email,
#                 js.phone,
#                 js.province,
#                 js.municipality,
#                 js.degree,
#                 js.portfolio_url,
#                 q.school_graduated,
#                 q.certifications,
#                 q.specialized_training,
#                 ji.job_interest,
#                 ji.job_type,
#                 ji.preferred_location,
#                 ji.expected_salary_range
#             FROM job_seekers js
#             LEFT JOIN qualifications q ON js.seeker_id = q.seeker_id
#             LEFT JOIN job_interest ji ON js.seeker_id = ji.user_id
#             WHERE js.email = %s
#         """, (email,))

#         result = cursor.fetchone()

#         if result:
#             # Convert the result to a dictionary
#             profile_data = {
#                 'first_name': result[0],
#                 'last_name': result[1],
#                 'email': result[2],
#                 'phone': result[3],
#                 'province': result[4],
#                 'municipality': result[5],
#                 'degree': result[6],
#                 'portfolio_url': result[7],
#                 'school_graduated': result[8],
#                 'certifications': result[9],
#                 'specialized_training': result[10],
#                 'job_interest': result[11],
#                 'job_type': result[12],
#                 'preferred_location': result[13],
#                 'expected_salary_range': result[14]
#             }
#             return json.dumps(profile_data)
#         else:
#             return json.dumps({'message': 'Profile not found'}), 404

#     except Exception as e:
#         print(f"Error fetching profile data: {e}")
#         return json.dumps({'message': 'Error fetching profile data'}), 500
#     finally:
#         if conn:
#             conn.close()