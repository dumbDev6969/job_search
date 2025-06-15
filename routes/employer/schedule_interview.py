
from sqlalchemy import text
from flask import Blueprint,render_template,session,request
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
from middlewares.is_requirements_done import is_requirements_done
from utils.check_if_exists import check_column_exists
from flask import jsonify
from utils.database import get_db

# Create a Blueprint
schedule_interview = Blueprint('schedule_interview', __name__)

# Define your routes using the Blueprint
@schedule_interview.route('/employer/schedule_interview/<int:application_id>', methods=['GET', 'POST'])
@verify_user
@is_email_verified
@is_requirements_done
def schedule_interview_(application_id):
    
            
    db = get_db()
    if not check_column_exists("applications", "application_id ", application_id ):
            return render_template("/pages/user_not_found.html")

    application_sql = text(f"SELECT * FROM applications WHERE application_id = {application_id}")
    application = db.execute_query(application_sql)
    if application['success']:
        if application['output']:
            job_id = application['output'][0]['job_id']
            employer_id = session['user_id']
            job_sql = text(f"SELECT * FROM jobs WHERE job_id = {job_id} AND  employer_id = {employer_id}")
            job_result = db.execute_query(job_sql)
            if not job_result['success'] or not job_result['output']:
                return render_template("/pages/user_not_found.html")
            return render_template('/pages/recruiter/schedule-interview.html', application=application['output'][0])
        else:
            return render_template("/pages/user_not_found.html")
    else:
        return render_template("/pages/user_not_found.html")


    # Define your routes using the Blueprint
@schedule_interview.route('/employer/api/schedule_interview', methods=['POST'])
@verify_user
@is_email_verified
@is_requirements_done
def schedule_interview_api():
    if request.method == 'POST':
        print("POST request received",request.form)
        form = request.form
    
        seeker_id = form.get('seeker_id')
        status = form.get('status')
        date = form.get('interview_date')
        time = form.get('interview_time')
        interview_type = form.get('interview_type')
        location = form.get('interview_location')
        gmeet_link = form.get('gmeet_link')
        additional_notes = form.get('additional_notes')
        status = form.get('status')


        if not all([ seeker_id, status, date, time, interview_type, location, status]):
            return jsonify({'error': 'Missing required fields'}), 400

        try:
            db = get_db()
            insert_sql = text("""
                INSERT INTO interviews ( seeker_id, status, date, time, interview_type, location, gmeet_link, additional_notes)
                VALUES ( :seeker_id, :status, :date, :time, :interview_type, :location, :gmeet_link, :additional_notes)
            """)
            result =  db.execute_query(insert_sql, {
              
                'seeker_id': seeker_id,
                'status': status,
                'date': date,
                'time': time,
                'interview_type': interview_type,
                'location': location,
                'gmeet_link': gmeet_link,
                'additional_notes': additional_notes,
            })
            if result['success']:
                print("Interview scheduled successfully")
                return jsonify({'message': 'Interview scheduled successfully','success':True,'status':201})
            else:
                print("Failed to schedule interview",result)
                return jsonify({'error': 'Failed to schedule interview'}), 500

        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return render_template('/pages/recruiter/schedule-interview.html')
