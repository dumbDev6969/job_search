from flask import Blueprint,render_template,jsonify,request
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
from utils.database import get_db
from sqlalchemy import text
from datetime import datetime
# Create a Blueprint
find_talent = Blueprint('find_talent', __name__)

# Define your routes using the Blueprint
@find_talent.route('/employer/find-talent')
@verify_user
@is_email_verified
def find_talent_():
    return render_template('/pages/recruiter/find_talent.html')
   
@find_talent.route('/api/employer/find-talent', methods=['GET', 'POST'])
@verify_user
@is_email_verified
def find_talent_api():
    try:
        db = get_db()
        
        # Get filter and pagination parameters
        name = request.args.get('name', '').strip()
        salary = request.args.get('salary', '').strip()
        location = request.args.get('location', '').strip()
        skills = request.args.get('skills', '').strip()
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        # Calculate offset
        offset = (page - 1) * per_page

        # Base query for counting total records
        count_query = """
            SELECT COUNT(DISTINCT js.seeker_id) as total
            FROM job_seekers js
            LEFT JOIN job_interest ji ON js.seeker_id = ji.user_id
            WHERE 1=1
        """

        # Base query for fetching records
        query = """
            SELECT 
                CONCAT(js.first_name, ' ', js.last_name) AS Name,
                'Available' AS Status,
                ji.job_interest AS Skills,
                CONCAT(ji.expected_salary_range, ' - ', ji.expected_salary_range) AS 'Salary Expectation',
                ji.preferred_location AS Location
            FROM job_seekers js
            LEFT JOIN job_interest ji ON js.seeker_id = ji.user_id
            WHERE 1=1
        """
        params = {}

        # Add filters
        if name:
            filter_condition = " AND (CONCAT(js.first_name, ' ', js.last_name) LIKE :name OR ji.job_interest LIKE :name)"
            query += filter_condition
            count_query += filter_condition
            params['name'] = f'%{name}%'

        if salary:
            filter_condition = " AND ji.expected_salary_range <= :salary"
            query += filter_condition
            count_query += filter_condition
            salary_value = ''.join(filter(str.isdigit, salary))
            params['salary'] = int(salary_value) if salary_value else 0

        if location:
            filter_condition = " AND ji.preferred_location LIKE :location"
            query += filter_condition
            count_query += filter_condition
            params['location'] = f'%{location}%'

        if skills:
            filter_condition = " AND ji.job_interest LIKE :skills"
            query += filter_condition
            count_query += filter_condition
            params['skills'] = f'%{skills}%'

        # Add pagination
        query += " GROUP BY js.seeker_id LIMIT :limit OFFSET :offset"
        params['limit'] = per_page
        params['offset'] = offset

        # Execute count query
        count_result = db.execute_query(text(count_query), params)
        total_records = count_result['output'][0]['total'] if count_result['success'] else 0
        total_pages = (total_records + per_page - 1) // per_page

        # Execute main query
        result = db.execute_query(text(query), params)

        if result['success']:
            talent_html = ""
            for talent in result['output']:
                talent_html += f"""<tr>
                    <td><input type="checkbox" class="form-check-input"></td>
                    <td>
                        <div class="d-flex align-items-center">
                            <img src="https://randomuser.me/api/portraits/men/32.jpg" 
                                class="rounded-circle me-2" width="36" height="36">
                            <div>
                                <div class="fw-bold">{talent['Name']}</div>
                                <small class="text-muted">Senior Frontend Developer</small>
                            </div>
                        </div>
                    </td>
                    <td><span class="badge bg-success">{talent['Status']}</span></td>
                    <td>
                        {' '.join([f'<span class="badge bg-light text-dark me-1">{skill.strip()}</span>' for skill in talent['Skills'].split(',') if skill.strip()])}
                    </td>
                    <td>{talent['Salary Expectation']}</td>
                    <td>{talent['Location']}</td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary">
                            <i class="fas fa-eye"></i>
                        </button>
                    </td>
                </tr>"""
            
            return jsonify({
                'talents': talent_html,
                'total_pages': total_pages,
                'current_page': page
            })
        else:
            return jsonify({
                'talents': "",
                'total_pages': 0,
                'current_page': 1
            })

    except Exception as e:
        print(e)
        return jsonify({'error': 'An error occurred while fetching job seekers.'}), 500