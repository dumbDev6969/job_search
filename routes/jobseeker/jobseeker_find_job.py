from flask import Blueprint,render_template,jsonify,request,redirect
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
from middlewares.is_setup_done import is_interests_done,is_qualification_done
from middlewares.user_access import jobseeker as job_seeker_middleware,admin,emplyer
from utils.database import get_db
from sqlalchemy import text

# Create a Blueprint
jobseeker_find_job = Blueprint('jobseeker_find_job', __name__)


@jobseeker_find_job.route('/jobseeker')
@jobseeker_find_job.route('/jobseeker/')
def redirect_to_jobseeker_dashboard():
    return redirect("/jobseeker/find-jobs")
    
@verify_user
# Define your routes using the Blueprint
@jobseeker_find_job.route('/jobseeker/find-jobs')
@verify_user
@is_email_verified
@is_qualification_done
@is_interests_done
@job_seeker_middleware
def jobseeker_find_job_():
    return render_template('/pages/job_seeker/find_jobs.html')

@jobseeker_find_job.route('/api/jobseeker/get-jobs')
@verify_user
def jobseeker_find_job_api():
    try:
        db = get_db()
        search_term = request.args.get('search', '')
        
        # Build the query with search functionality
        query = text("""
            SELECT j.*, e.company_name 
            FROM jobs j 
            JOIN employers e ON j.employer_id = e.employer_id 
            WHERE j.status = 'active'
            AND (
                LOWER(j.title) LIKE :search 
                OR LOWER(j.description) LIKE :search
                OR LOWER(e.company_name) LIKE :search
            )
        """)
        
        # Execute query with search parameter
        search_param = f"%{search_term.lower()}%"
        result = db.execute_query(query, {'search': search_param})
        
        if not result['success']:
            print(result['error'])
            return jsonify({'error': 'Failed to fetch jobs'}), 500
            
        jobs = result['output']
        html_cards = []
        
        for job in jobs:
            card = f"""
            <div class="col-md-4 col-job-card">
                <div class="job-card p-3 mb-3 d-flex flex-column">
                    <div class="d-flex align-items-center">
                        <img src="/assets/img/default_profile.jpg" alt="Company Logo" class="company-logo me-3">
                        <div>
                            <h5 class="company-name">{job['company_name']}</h5>
                            <p class="job-type badge">{job['employment_type']}</p>
                        </div>
                    </div>
                    <h4 class="job-title mt-3">{job['title']}</h4>
                    <p class="salary-range text-secondary">{job['salary_range']}</p>
                    <p class="location"><i class="fas fa-map-marker-alt"></i> {job['location']}</p>
                    <div class="mt-auto d-flex justify-content-between gap-2">
                        <button class="btn-primary w-100 rounded">Apply Now</button>
                        <button class="btn-outline-secondary rounded">Save</button>
                    </div>
                </div>
            </div>
            """
            html_cards.append(card)
        
        return ''.join(html_cards)
        
    except Exception as e:
        print(e)
        return jsonify({'error': str(e)}), 500