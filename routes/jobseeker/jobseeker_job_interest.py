from flask import Blueprint,render_template,jsonify,request,session
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
from middlewares.is_setup_done  import interests_done
from utils.database import get_db
from sqlalchemy import text
from utils.check_if_exists import check_column_exists
jobseeker_job_interest = Blueprint('jobseeker_job_interest', __name__)

# Define your routes using the Blueprint
@jobseeker_job_interest.route('/jobseeker/job-interest')
@verify_user
@is_email_verified
@interests_done
def jobseeker_job_interest_():
    """Render the job seeker's job interest page.

    This route displays the page where job seekers can view and manage their
    job interests and preferences. Access requires user authentication
    and email verification.

    Decorators:
        @verify_user: Ensures the user is authenticated
        @is_email_verified: Ensures the user's email is verified

    Returns:
        rendered template: The job seeker job interest HTML page
    """
    return render_template('/pages/job_seeker/job_interest.html')



@jobseeker_job_interest.route('/jobseeker/api/job-interest', methods=['POST'])
@verify_user
def job_interest_api():
    try:
        data = request.form
        seeker_id = session['user_id']
        # Check if job interest already exists for the seeker
        if check_column_exists('job_interest', 'user_id', seeker_id):
            return jsonify({'error': 'Job interest already exists'}), 400
         
        # Validate required fields
        required_fields = ['job_interest', 'job_type', 'preferred_location', 'expected_salary_range']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'{field.replace("_", " ").title()} is required'}), 400
        
        # Get database connection
        db = get_db()
        
        # Insert job interest data
        query = text("""
            INSERT INTO job_interest 
            (user_id, job_interest, job_type, preferred_location, expected_salary_range)
            VALUES (:user_id, :job_interest, :job_type, :preferred_location, :expected_salary_range)
        """)
        
        db.execute_query(query, {
            'user_id': seeker_id,
            'job_interest': data.get('job_interest'),
            'job_type': data.get('job_type'),
            'preferred_location': data.get('preferred_location'),
            'expected_salary_range': data.get('expected_salary_range')
        })
        
        return jsonify({'success': True,'message': 'Job interest added successfully'}), 201
        
    except Exception as e:
        print(f"Error adding job interest: {str(e)}")
        return jsonify({'error': str(e)}), 500


@jobseeker_job_interest.route('/jobseeker/api/job-interest', methods=['GET'])
@verify_user
def get_job_interest():
    """Retrieve job interest information for the current job seeker.
    
    This route fetches the job interest details for the authenticated job seeker
    from the database.
    
    Returns:
        JSON response containing job interest data or error message
    """
    try:
        seeker_id = session['user_id']
        
        # Get database connection
        db = get_db()
        
        # Query to fetch job interest data
        query = text("""
            SELECT job_interest, job_type, preferred_location, expected_salary_range 
            FROM job_interest 
            WHERE user_id = :user_id
        """)
        
        # Execute query and fetch results
        result = db.execute_query(query, {'user_id': seeker_id})
        
        if result:
            return jsonify(result['output'][0]), 200
        else:
            return jsonify({'message': 'No job interest found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
