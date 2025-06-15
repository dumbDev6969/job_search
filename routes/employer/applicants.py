from flask import Blueprint,render_template
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
from middlewares.is_requirements_done import is_requirements_done
from utils.database import get_db
from sqlalchemy import text
from flask import jsonify, session

# Create a Blueprint
applicants = Blueprint('applicants', __name__)

# Define your routes using the Blueprint
@applicants.route('/employer/applicants')
@verify_user
@is_email_verified
@is_requirements_done
def applicants_():
    return render_template('/pages/recruiter/applicants.html')

@applicants.route('/api/employer/applicants', methods=['GET'])
@verify_user
@is_email_verified
@is_requirements_done
def get_applicants():
    try:
        db = get_db()

        # Base query for fetching records
        query = """
            SELECT
    CONCAT(js.first_name, ' ', js.last_name) AS Name,
    j.title AS Position,
    a.status AS Status
FROM applications a
LEFT JOIN job_seekers js ON a.seeker_id = js.seeker_id
LEFT JOIN jobs j ON a.job_id = j.job_id
WHERE j.employer_id = :employer_id;
        """

        # Execute main query
        result = db.execute_query(text(query),  {"employer_id": session.get('user_id')})
        if result['success']:
            interviews_html = ""

            if not result['output']:
                return jsonify({
                    'applications': """
        <tr>
            <td colspan="7" class="text-center py-4">
                <div class="d-flex flex-column align-items-center">
                    <i class="fas fa-search fa-3x text-muted mb-3"></i>
                    <h5 class="text-muted">No listings found</h5>
                    <p class="text-muted">There are currently no candidates to display.</p>
                </div>
            </td>
        </tr>
    """
                })
            print(result['output']) 
            for interview in result['output']:
                interview_html = f"""<tr>
                    <td>
                        <div class="d-flex align-items-center">
                            <img src="https://randomuser.me/api/portraits/men/32.jpg" class="rounded-circle me-2" width="36" height="36">
                            <div>
                                <h6 class="mb-0">{interview['Name']}</h6>
                              
                            </div>
                        </div>
                    </td>
                    <td> {interview['Position']}</td>
                    <td><span class="badge bg-info">{interview['Status']}</span></td>
                   
                </tr>"""
                interviews_html += interview_html

            return jsonify({
                'applications': interviews_html
            })
        else:
            return jsonify({
                'applications': ""
            })

    except Exception as e:
        print(e)
        return jsonify({'error': 'An error occurred while fetching interviews.'}), 500

