from flask import Blueprint,render_template,jsonify,request, session
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
from middlewares.is_requirements_done import is_requirements_done

from utils.database import get_db
from sqlalchemy import text
import logging
# Create a Blueprint
find_talent = Blueprint('find_talent', __name__)

# Define your routes using the Blueprint
@find_talent.route('/employer/find-talent')
@verify_user
@is_email_verified
@is_requirements_done
def find_talent_():
    return render_template('/pages/recruiter/find_talent.html')
   


@find_talent.route('/api/employer/find-talent', methods=['GET', 'POST'])
@verify_user
@is_email_verified
@is_requirements_done
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
            INNER JOIN applications app ON js.seeker_id = app.seeker_id
            INNER JOIN jobs j ON app.job_id = j.job_id
            LEFT JOIN job_interest ji ON js.seeker_id = ji.user_id
            WHERE j.employer_id = :employer_id
        """

        # Base query for fetching records
        query = """
            SELECT 
                js.seeker_id, /* Adding for potential use, and for GROUP BY */
                CONCAT(js.first_name, ' ', js.last_name) AS Name,
                'Available' AS Status,
                ji.job_interest AS Skills,
                CONCAT(ji.expected_salary_range, ' - ', ji.expected_salary_range) AS 'Salary Expectation',
                ji.preferred_location AS Location
            FROM job_seekers js
            INNER JOIN applications app ON js.seeker_id = app.seeker_id
            INNER JOIN jobs j ON app.job_id = j.job_id
            LEFT JOIN job_interest ji ON js.seeker_id = ji.user_id
            WHERE j.employer_id = :employer_id
        """
        params = {
            'employer_id': session['user_id']
        }

        # Add filters
        if name:
            filter_condition = " AND (CONCAT(js.first_name, ' ', js.last_name) LIKE :name OR (ji.job_interest IS NOT NULL AND ji.job_interest LIKE :name))"
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
            filter_condition = " AND (ji.preferred_location IS NOT NULL AND ji.preferred_location LIKE :location)"
            query += filter_condition
            count_query += filter_condition
            params['location'] = f'%{location}%'

        if skills:
            filter_condition = " AND (ji.job_interest IS NOT NULL AND ji.job_interest LIKE :skills)"
            query += filter_condition
            count_query += filter_condition
            params['skills'] = f'%{skills}%'

        # Add pagination
        query += " GROUP BY js.seeker_id LIMIT :limit OFFSET :offset"
        params['limit'] = per_page
        params['offset'] = offset

        # Log queries and parameters
        logging.debug(f"Count Query: {count_query}")
        logging.debug(f"Main Query: {query}")
        logging.debug(f"Parameters: {params}")

        # Execute count query
        count_result = db.execute_query(text(count_query), params)
        total_records = 0
        if count_result['success'] and count_result['output']:
            total_records = count_result['output'][0]['total']
        else:
            logging.error(f"Count Query Execution Failed: {count_result.get('error', 'Unknown error')}")
        total_pages = (total_records + per_page - 1) // per_page

        # Execute main query
        result = db.execute_query(text(query), params)
        logging.warning(f"Main Query Result: {result}")
        if result['success']:

            talent_html = ""
            logging.debug(f"Main Query Result: {result['output']}")
            for talent in result['output']:
                skills = talent.get('Skills', '')
                skill_badges = ''.join(
                    f'<span class="badge bg-light text-dark me-1">{skill.strip()}</span>'
                    for skill in skills.split(',') if skill.strip()
                )
                first_skill = skills.split(',')[0] if skills else ''
                
                talent_html += f"""<tr>
                    <td><input type="checkbox" class="form-check-input"></td>
                    <td>
                        <div class="d-flex align-items-center">
                            <img src="https://randomuser.me/api/portraits/men/32.jpg" 
                                class="rounded-circle me-2" width="36" height="36">
                            <div>
                                <div class="fw-bold">{talent['Name']}</div>
                                <small class="text-muted">{first_skill}</small>
                            </div>
                        </div>
                    </td>
                    <td><span class="badge bg-success">Available</span></td>
                    <td>{skill_badges}</td>
                    <td>{talent['Salary Expectation']}</td>
                    <td>{talent['Location'] or 'N/A'}</td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary">
                            <i class="fas fa-eye"></i>
                        </button>
                    </td>
                </tr>"""
            logging.warning(f"Talent HTML: {talent_html}")
            return jsonify({
                'html': talent_html, # The frontend expects 'html' for table content based on find_talent.html
                'total_pages': total_pages,
                'current_page': page,
                'total_records': total_records
            })
        else:
            logging.error(f"Main Query Execution Failed: {result.get('error', 'Unknown error')}")
            return jsonify({
                'html': "",
                'total_pages': 0,
                'current_page': 1
            })

    except Exception as e:
        logging.exception("An error occurred while fetching job seekers.")
        return jsonify({'error': 'An error occurred while fetching job seekers.'}), 500
