
from flask import Blueprint,render_template,session,jsonify,request
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
from utils.database import get_db
from sqlalchemy import text

# Create a Blueprint
jobs = Blueprint('jobs', __name__)

# Define your routes using the Blueprint
@jobs.route('/employer/jobs')
@verify_user
@is_email_verified
def jobs_():
    return render_template('/pages/recruiter/jobs.html')





@jobs.route('/api/post-job',methods=['POST'])
def post_job_api():
    try:
        db = get_db()
        
        query = text("""
            INSERT INTO jobs 
            (employer_id, title, description, location, salary_range, 
             employment_type, expires_at, status)
            VALUES 
            (:employer_id, :title, :description, :location, :salary_range,
             :employment_type, :expires_at, :status)
        """)
        
        # Get form data from request
        form_data = request.form
        
        result = db.execute_query(query, {
            'employer_id': session.get('user_id'),
            'title': form_data.get('title'),
            'description': form_data.get('description'),
            'location': form_data.get('location'),
            'salary_range': form_data.get('salary_range'),
            'employment_type': form_data.get('employment_type'),
            'expires_at': form_data.get('expires_at'),
            'status': 'active'
        })
        
        if result['success']:
            return jsonify({'message': 'Job posted successfully'}), 201
        else:
            return jsonify({'error': 'Job posting failed', 'details': result['message']}), 400
            
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'error': 'Job posting failed', 'details': str(e)}), 500


@jobs.route('/employer/post-job')
@verify_user
@is_email_verified
def post_job_():
    return render_template('/pages/recruiter/post_job.html')