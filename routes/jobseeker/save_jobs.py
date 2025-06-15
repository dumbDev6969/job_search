from flask import Blueprint,render_template,jsonify,request,redirect,session
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
from middlewares.is_setup_done import is_interests_done,is_qualification_done
from middlewares.user_access import jobseeker as job_seeker_middleware,admin,emplyer
from utils.database import get_db
from sqlalchemy import text
import datetime

# Create a Blueprint
save_job = Blueprint('save_job', __name__)

@save_job.route('/api/jobseeker/get-saved-jobs', methods=['GET'])
@verify_user
def get_saved_jobs():
    seeker_id = session.get('user_id')
    search_term = request.args.get('search', '')
  
    db = get_db()
    try:
        query = text("""
           SELECT j.*,e.* 
FROM saved_jobs sj
JOIN jobs j ON sj.job_id = j.job_id
JOIN employers e ON j.employer_id = e.employer_id
WHERE sj.seeker_id = :seeker_id and (:search_term = '' OR j.title LIKE CONCAT('%', :search_term, '%'))
        """)
        
        result = db.execute_query(query, {'seeker_id': seeker_id,'search_term':search_term})
        
        if not result['success'] or not result['output']:
            
            return """
            <div class="container mt-5">
                <div class="row justify-content-center">
                    <div class="col-md-8 text-center">
                        <div class="alert alert-info" role="alert">
                            <h4 class="alert-heading">No Saved Jobs Found</h4>
                            <p>You haven't saved any jobs yet. Start exploring and save jobs that interest you!</p>
                            <hr>
                            <p class="mb-0">Browse available jobs to find opportunities that match your skills and interests.</p>
                        </div>
                    </div>
                </div>
            </div>
            """
            
        html_cards = []
        for job in result['output']:

          
            card = f"""
              <div class="row align-items-center"  >
            <!-- Profile Image -->
            <div class="col-md-2 d-flex justify-content-center">
                <img class="rounded-circle" src="/assets/img/default_profile.jpg" alt="default_profile" height="100">
            </div>
            
            <!-- Job Details -->
            <div class="col-md-10">
                <div class="row">
                    <div class="col-md-12 d-flex justify-content-between align-items-center" id="saved_jobs_container">
                        <div class="name d-flex align-items-center">
                            <h3 class="mb-0">{job['title']}</h3>
                            <p class="badge rounded-pill text-bg-primary ms-3 job-status d-flex align-items-center">{job['status']}</p>
                        </div>
                        <div class="d-flex flex-column gap-2">
                            <button type="button" class="btn-danger" onclick="removeSavedJob({job['job_id']})">Remove</button>
                            <button type="button" class="btn-primary" onclick="window.location.href='/jobseeker/view-job/{job['job_id']}'">View</button>
                        </div>
                    </div>
    
                    <div class="col-md-12">
                        <p class="text-secondary mb-1">{job['company_name']}</p>
                        <div class="d-flex flex-wrap gap-2">
                            <span class="badge rounded-pill text-bg-primary job-info">{job['location']}</span>
                            <span class="badge rounded-pill text-bg-primary job-info">{job['salary_range']}</span>
                            <span class="badge rounded-pill text-bg-primary job-info">{job['employment_type']}</span>
                        </div>
                    </div>
                </div>
            </div>
            </div>

            """
            html_cards.append(card)
            
        return ''.join(html_cards)
        
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500

        
@save_job.route('/jobseeker/view-job/<int:job_id>', methods=['GET'])
@verify_user
def view_saved_job(job_id):
    seeker_id = session.get('user_id')
    db = get_db()
    
    # Query job and employer details
    query = text("""
        SELECT j.*, e.*
        FROM jobs j
        JOIN employers e ON j.employer_id = e.employer_id
        WHERE j.job_id = :job_id
    """)
    
    result = db.execute_query(query, {'job_id': job_id})
    
    if not result['success'] or not result['output']:
        return "Job not found", 404
    
    job_data = result['output'][0]
    
    # Format employment type for display
    if job_data['employment_type'] == 'full_time':
        job_data['employment_type'] = "Full Time"
    elif job_data['employment_type'] == 'part_time':
        job_data['employment_type'] = "Part Time"
    elif job_data['employment_type'] == 'contract':
        job_data['employment_type'] = "Contract"
    elif job_data['employment_type'] == 'internship':
        job_data['employment_type'] = "Internship"
    
    # Ensure all required fields are present
    job_data['status'] = job_data.get('status', 'Active')
    job_data['title'] = job_data.get('title', '')
    job_data['company_name'] = job_data.get('company_name', '')
    job_data['company_logo'] = job_data.get('company_logo', '')
    job_data['location'] = job_data.get('location', '')
    job_data['company_size'] = job_data.get('company_size', '')
    job_data['salary'] = job_data.get('salary', '')
    job_data['experience'] = job_data.get('experience', '')
    job_data['deadline'] = job_data.get('deadline', '')
    job_data['description'] = job_data.get('description', '')
    job_data['company_website'] = job_data.get('company_website', '')
    job_data['linkedin_url'] = job_data.get('linkedin_url', '')
    job_data['posted_date'] = job_data.get('posted_date', datetime.datetime.now().isoformat())
    
    return render_template('/pages/job-details.html', job=job_data)

@save_job.route('/api/jobseeker/remove-job', methods=['POST'])
@verify_user
def remove_saved_job():
    seeker_id = session.get('user_id')
    job_id = request.form.get('job_id')
    if not seeker_id:
        return jsonify({'error': 'Missing user ID'}), 400
    
    db = get_db()
    try:
        query = text("""
            DELETE FROM saved_jobs 
            WHERE seeker_id = :seeker_id AND job_id = :job_id
        """)
        
        result = db.execute_query(query, {'seeker_id': seeker_id, 'job_id': job_id})
        
        if result['success']:
            return jsonify({'success': True, 'message': 'Job removed successfully'})
        else:
            return jsonify({'error': 'Failed to remove job'}), 500
            
    except Exception as e:
      
        return jsonify({'error': str(e)}), 500

@save_job.route('/api/jobseeker/save-job', methods=['POST'])
@verify_user
def save_job_():
    job_id = request.form.get('job_id')
    seeker_id = session.get('user_id')
    
    if not job_id or not seeker_id:
        return jsonify({'error': 'Missing required parameters'}), 400
    
    db = get_db()
    try:
        query = text("""
            INSERT INTO saved_jobs (seeker_id, job_id)
            VALUES (:seeker_id, :job_id)
        """)
     
        db.execute_query(query, {'seeker_id': seeker_id, 'job_id': job_id})
        
        return jsonify({'success': True, 'message': 'Job saved successfully'})
    except Exception as e:
      
        return jsonify({'error': str(e)}), 500