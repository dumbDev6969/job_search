from flask import Blueprint, render_template, request, jsonify,session
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
from middlewares.user_access import jobseeker as job_seeker_middleware,admin,emplyer
from utils.database import get_db
from sqlalchemy import text
from middlewares.is_setup_done  import qualification_done
from utils.check_if_exists import check_column_exists

# Create a Blueprint
jobseeker_qualification = Blueprint('jobseeker_qualification', __name__)

# Define your routes using the Blueprint
@jobseeker_qualification.route('/jobseeker/qualification', methods=['GET'])
@verify_user
@is_email_verified
@qualification_done
def jobseeker_qualification_():
    """Render the job seeker's qualification page.

    This route displays the page where job seekers can view and manage their
    qualifications, skills, and experience. Access requires user authentication
    and email verification.

    Decorators:
        @verify_user: Ensures the user is authenticated
        @is_email_verified: Ensures the user's email is verified

    Returns:
        rendered template: The job seeker qualification HTML page
    """
    return render_template('/pages/job_seeker/qualification.html')

@jobseeker_qualification.route('/jobseeker/api/qualification', methods=['POST'])
@verify_user
def add_qualification():
    """Handle qualification form submission.
    
    This route accepts POST requests with qualification data and inserts it into the database.
    Required fields: degree, school_graduated
    Optional fields: certifications, specialized_training
    
    Returns:
        JSON response indicating success or failure
    """
    try:
        data = request.form
        seeker_id =session['user_id'] # Assuming user_id is set by verify_user middleware
        if check_column_exists('qualifications','seeker_id',seeker_id):
            return jsonify({'error': 'Qualification already exists'}), 400
        
        # Validate required fields
        if not data.get('degree') or not data.get('school_graduated'):
            return jsonify({'error': 'Degree and school graduated are required'}), 400
            
        # Get database connection
        db = get_db()
        
        # Insert qualification data
        query = text("""
            INSERT INTO qualifications 
            (seeker_id, degree, school_graduated, certifications, specialized_training)
            VALUES (:seeker_id, :degree, :school_graduated, :certifications, :specialized_training)
        """)
        
        db.execute_query(query, {
            'seeker_id': seeker_id,
            'degree': data.get('degree'),
            'school_graduated': data.get('school_graduated'),
            'certifications': data.get('certifications'),
            'specialized_training': data.get('specialized_training')
        })
        
        return jsonify({'success': True,'message': 'Qualification added successfully'}), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@jobseeker_qualification.route('/jobseeker/api/qualification', methods=['GET'])
@verify_user
def get_qualification():
    """Retrieve qualification information for the current job seeker.
    
    This route fetches the qualification details for the authenticated job seeker
    from the database.
    
    Returns:
        JSON response containing qualification data or error message
    """
    try:
        seeker_id = session['user_id']
        
        # Get database connection
        db = get_db()
        
        # Query to fetch qualification data
        query = text("""
            SELECT degree, school_graduated, certifications, specialized_training 
            FROM qualifications 
            WHERE seeker_id = :seeker_id
        """)
        
        # Execute query and fetch results
        result = db.execute_query(query, {'seeker_id': seeker_id})
        
        if result:
            return jsonify(result['output'][0]), 200
        else:
            return jsonify({'message': 'No qualification found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500
