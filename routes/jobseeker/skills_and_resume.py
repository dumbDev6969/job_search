from flask import Blueprint, render_template, request, session, jsonify, send_from_directory
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
from middlewares.user_access import jobseeker, admin, emplyer  # double-check typo?
from middlewares.is_setup_done import is_interests_done, is_qualification_done
from middlewares.skills_and_resume import is_skills_and_resume_done
from utils.database import get_db
from sqlalchemy import text
import os
from werkzeug.utils import secure_filename

# Create Blueprint
jobseeker_skills_and_resume = Blueprint('jobseeker_skills_and_resume', __name__)

# Define upload folder (relative path)
UPLOAD_FOLDER = 'files/resumes'

def save_file(file, upload_folder):
    """Saves a file to the server and returns its saved path."""
    if not file or file.filename == '':
        return None

    try:
        # Ensure the upload directory exists
        upload_path = os.path.join("files", upload_folder)
        os.makedirs(upload_path, exist_ok=True)

        # Generate a safe filename
        filename = secure_filename(file.filename)
        file_path = os.path.join(upload_path, filename)

        # Save the file
        file.save(file_path)

        # Return relative path (assumes files are served from a static/files folder)
        return "/" + file_path  # Or adjust based on how you serve files

    except Exception as e:
        print(f"Error saving file: {str(e)}")
        return None


# Route to render the form
@jobseeker_skills_and_resume.route('/jobseeker/skills-and-resume')
@verify_user
@is_email_verified
@is_interests_done
@is_qualification_done
def jobseeker_skills_and_resume_():
    return render_template('/pages/job_seeker/skills_resume.html')


# API Route to handle form submission
@jobseeker_skills_and_resume.route('/api/jobseeker/skills-and-resume', methods=['POST'])
@verify_user
def upload_skills_and_resume():
    form = request.form
    files = request.files

    about = form.get('about')
    experience_title = form.get('experience')
    company = form.get('company')
    experience_date = form.get('experience-date')
    experience_description = form.get('experience-description')
    resume_file = files.get('resume')
    linkedin = form.get('linkedin')
    github = form.get('github')
    twitter = form.get('twitter')
    if not all([about]):
        return jsonify({'error': 'Missing required fields'}), 400

    seeker_id = session.get('user_id')
    if not seeker_id:
        return jsonify({'error': 'User not logged in'}), 401

    # Save resume using your custom save_file function
    resume_path = save_file(resume_file, UPLOAD_FOLDER)

    db = get_db()
    try:
        query = text("""
            INSERT INTO seeker_profiles (
                user_id, about, experience_title, company,
                experience_date, experience_description, resume,
                linkedin, github, twitter
            ) VALUES (
                :user_id, :about, :experience_title, :company,
                :experience_date, :experience_description, :resume,
                :linkedin, :github, :twitter
            )
          
        """) 
        #   ON CONFLICT (user_id) DO UPDATE SET
        #         about = EXCLUDED.about,
        #         experience_title = EXCLUDED.experience_title,
        #         company = EXCLUDED.company,
        #         experience_date = EXCLUDED.experience_date,
        #         experience_description = EXCLUDED.experience_description,
        #         resume = EXCLUDED.resume,
        #         linkedin = EXCLUDED.linkedin,
        #         github = EXCLUDED.github,
        #         twitter = EXCLUDED.twitter

        result = db.execute_query(query, {
            'user_id': seeker_id,
            'about': about,
            'experience_title': experience_title,
            'company': company,
            'experience_date': experience_date,
            'experience_description': experience_description,
            'resume': resume_path,
            'linkedin': linkedin,
            'github': github,
            'twitter': twitter
        })
        if result['success']:
            return jsonify({'message': 'Skills and resume updated successfully!', 'success': True, 'status': 200}), 200
        else:
            print(result)
            return jsonify({'error': 'Failed to update skills and resume',  'success': False, 'status': 500}), 500


    except Exception as e:
        return jsonify({'error': str(e)}), 500


# API Route to fetch data
@jobseeker_skills_and_resume.route('/api/jobseeker/skills-and-resume', methods=['GET'])
@verify_user
def get_skills_and_resume():
    try:
        seeker_id = session['user_id']
        db = get_db()

        query = text("""
            SELECT about, experience_title, company, experience_date, experience_description, resume, linkedin, github, twitter
            FROM seeker_profiles
            WHERE user_id = :user_id
        """)

        result = db.execute_query(query, {'user_id': seeker_id})

        if result and result['output']:
            return jsonify(result['output'][0]), 200
        else:
            return jsonify({'message': 'No skills and resume data found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500