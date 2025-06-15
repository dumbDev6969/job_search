from flask import Blueprint, render_template, jsonify, request,session
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
from middlewares.is_requirements_done import is_requirements_done
from utils.database import get_db
from sqlalchemy import text
from datetime import datetime

# Create a Blueprint
schedule_dashboard = Blueprint('schedule_dashboard', __name__)

# Define your routes using the Blueprint
@schedule_dashboard.route('/employer/schedule_dashboard')
@verify_user
@is_email_verified
@is_requirements_done
def schedule_dashboard_():
    return render_template('/pages/recruiter/schedule-dashboard.html')

@schedule_dashboard.route('/api/employer/schedule-dashboard-no-filters', methods=['GET', 'POST'])
@verify_user
@is_email_verified
@is_requirements_done
def schedule_dashboard_api_no_filters():
    try:
        db = get_db()

        # Base query for fetching records
        query = """
        SELECT
    CONCAT(js.first_name, ' ', js.last_name) AS Name,
    i.date AS InterviewDate,
    i.time AS InterviewTime,
    i.interview_type AS InterviewType,
    i.location AS LocationOrMeetLink,
    i.status AS Status,
    i.gmeet_link AS GoogleMeetLink,
    i.additional_notes AS AdditionalNotes
FROM interviews i
LEFT JOIN job_seekers js ON i.seeker_id = js.seeker_id
INNER JOIN applications a ON i.seeker_id = a.seeker_id
INNER JOIN jobs j ON a.job_id = j.job_id
WHERE i.status != 'scheduled'
  AND j.employer_id = :employer_id;
        """
        
        # Execute main query
        result = db.execute_query(text(query),  {"employer_id": session.get('user_id')})
        print(result['output'])
        if result['success']:
           
            interviews_html = ""
            
            if not result['output']:
                print("no in candidates found")
                return jsonify({
                    'interviews': """
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

            for interview in result['output']:
                interview_html = f"""<tr>
                    <td>
                        <div class="d-flex align-items-center">
                            <img src="https://randomuser.me/api/portraits/men/32.jpg" class="rounded-circle me-2" width="36" height="36">
                            <div>
                                <h6 class="mb-0">{interview['Name']}</h6>
                                <small class="text-muted">Senior Frontend Dev</small>
                            </div>
                        </div>
                    </td>
                    <td>Senior Frontend</td>
                    <td><span class="badge bg-warning">Technical Review</span></td>
                    <td>
                        <button class="btn btn-sm btn-info">View</button>
                        <button class="btn btn-sm btn-primary">Schedule Interview</button>
                    </td>
                </tr>"""
                interviews_html += interview_html

            return jsonify({
                'interviews': interviews_html
            })
        else:
            return jsonify({
                'interviews': ""
            })

    except Exception as e:
        print(e)
        return jsonify({'error': 'An error occurred while fetching interviews.'}), 500
@schedule_dashboard.route('/api/employer/schedule-dashboard', methods=['GET', 'POST'])
@verify_user
@is_email_verified
@is_requirements_done
def schedule_dashboard_api():
    try:
        db = get_db()

        # Get filter and pagination parameters
        name = request.args.get('name', '').strip()
        date = request.args.get('date', '').strip()
        time = request.args.get('time', '').strip()
        type = request.args.get('type', '').strip()
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        # Calculate offset
        offset = (page - 1) * per_page

        # Base query for counting total records
        count_query = """
            SELECT COUNT(DISTINCT i.interview_id) as total
            FROM interviews i
            LEFT JOIN job_seekers js ON i.seeker_id = js.seeker_id
            WHERE 1=1
        """

        # Base query for fetching records
        query = """
           SELECT
    CONCAT(js.first_name, ' ', js.last_name) AS Name,
    i.date AS InterviewDate,
    i.time AS InterviewTime,
    i.interview_type AS InterviewType,
    i.location AS LocationOrMeetLink,
    i.status AS Status,
    i.gmeet_link AS GMeetLink,
    i.additional_notes AS AdditionalNotes,
    i.interview_id AS InterviewId
FROM interviews i
LEFT JOIN job_seekers js ON i.seeker_id = js.seeker_id
INNER JOIN applications a ON i.seeker_id = a.seeker_id
INNER JOIN jobs j ON a.job_id = j.job_id
WHERE j.employer_id = :employer_id;
        """
        params = {}

        # Add filters
        if name:
            filter_condition = " AND (CONCAT(js.first_name, ' ', js.last_name) LIKE :name)"
            query += filter_condition
            count_query += filter_condition
            params['name'] = f'%{name}%'

        if date:
            filter_condition = " AND i.date = :date"
            query += filter_condition
            count_query += filter_condition
            params['date'] = date

        if time:
            filter_condition = " AND i.time = :time"
            query += filter_condition
            count_query += filter_condition
            params['time'] = time

        if type:
            filter_condition = " AND i.interview_type LIKE :type"
            query += filter_condition
            count_query += filter_condition
            params['type'] = f'%{type}%'
       

        # Add pagination
        query += " GROUP BY i.interview_id LIMIT :limit OFFSET :offset"
        params['limit'] = per_page
        params['offset'] = offset
        params['employer_id'] = session.get('user_id')


        # Execute count query
        count_result = db.execute_query(text(count_query), params)
        total_records = count_result['output'][0]['total'] if count_result['success'] else 0
        total_pages = (total_records + per_page - 1) // per_page

        # Execute main query
        result = db.execute_query(text(query), params)
        if result['success']:
            interviews_html = ""
            print(result['output'])
            for interview in result['output']:
                interview_html = f"""<tr>
                    <td>{interview['InterviewId']}</td>
                    <td>
                        <div class="d-flex align-items-center">
                            <img src="https://randomuser.me/api/portraits/men/32.jpg"
                                class="rounded-circle me-2" width="36" height="36">
                            <div>
                                <div class="fw-bold">{interview['Name']}</div>
                            </div>
                        </div>
                    </td>
                    <td>{interview['InterviewDate']}</td>
                    <td>{interview['InterviewTime']}</td>
                    <td>{interview['InterviewType']}</td>
                    <td>{interview['LocationOrMeetLink']}</td>
                    <td>
                        <span class="badge bg-success">{interview['Status']}</span>
                    </td>
                    <td>
                        <div class="gap-2">
                            <button class="btn btn-sm btn-outline-primary" title="View Details">
                                <i class="fas fa-eye"></i>
                            </button>
                            <button class="btn btn-sm btn-outline-secondary" title="Edit">
                                <i class="fas fa-edit"></i>
                            </button>
                            <button class="btn btn-sm btn-outline-danger" title="Cancel">
                                <i class="fas fa-times"></i>
                            </button>
                        </div>
                    </td>
                </tr>"""
                interviews_html += interview_html

            return jsonify({
                'interviews': interviews_html,
                'total_pages': total_pages,
                'current_page': page,
                'total_records': total_records
            })
        else:
            return jsonify({
                'interviews': "",
                'total_pages': 0,
                'current_page': 1
            })

    except Exception as e:
        print(e)
        return jsonify({'error': 'An error occurred while fetching interviews.'}), 500
    




@schedule_dashboard.route('/api/employer/upcoming-interviews', methods=['GET', 'POST'])
@verify_user
@is_email_verified
@is_requirements_done
def schedule_dashboard_api_upcoming_interviews():
    try:
        db = get_db()

        # Base query for fetching records
        query = """
      SELECT DISTINCT
    CONCAT(js.first_name, ' ', js.last_name) AS Name,
    i.date AS InterviewDate,
    i.time AS InterviewTime,
    i.interview_type AS InterviewType,
    COALESCE(i.location, i.gmeet_link) AS LocationOrMeetLink,
    i.status AS Status,
    i.gmeet_link AS GoogleMeetLink,
    i.additional_notes AS AdditionalNotes
FROM 
    interviews i
INNER JOIN 
    job_seekers js ON i.seeker_id = js.seeker_id
INNER JOIN 
    applications a ON i.seeker_id = a.seeker_id
INNER JOIN 
    jobs j ON a.job_id = j.job_id
WHERE 
    i.status = 'scheduled' AND i.employer_id = :employer_id
ORDER BY 
    i.date ASC, i.time ASC;
        """
        
        # Execute main query
        result = db.execute_query(text(query),   {"employer_id": session.get('user_id')})
        print("uppcoming interviews",result['output'])
        if result['success']:
           
            interviews_html = ""
            
            if not result['output']:
                print("no in intervies found")
                return jsonify({
                    'interviews': """
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
                    <td>{interview['InterviewDate']}</td>
                    <td><span class="badge bg-warning">{interview['InterviewTime']}</span></td>
                    <td>
                       {interview['InterviewType']}
                    </td>
                    <td>    
                        {interview['LocationOrMeetLink']}
                    </td>
                </tr>"""
                interviews_html += interview_html

            return jsonify({
                'interviews': interviews_html
            })
        else:
            return jsonify({
                'interviews': ""
            })

    except Exception as e:
        print(e)
        return jsonify({'error': 'An error occurred while fetching interviews.'}), 500
