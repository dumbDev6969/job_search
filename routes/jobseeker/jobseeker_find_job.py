from flask import Blueprint, render_template, jsonify, request, redirect, session
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
from middlewares.is_setup_done import is_interests_done, is_qualification_done
from middlewares.user_access import jobseeker as job_seeker_middleware, admin, emplyer
from utils.database import get_db
from sqlalchemy import text
from flask_wtf.csrf import generate_csrf
from middlewares.skills_and_resume import is_skills_and_resume_done

# Create a Blueprint
jobseeker_find_job = Blueprint("jobseeker_find_job", __name__)


@jobseeker_find_job.route("/jobseeker")
@jobseeker_find_job.route("/jobseeker/")
def redirect_to_jobseeker_dashboard():
    return redirect("/jobseeker/find-jobs")


# Define your routes using the Blueprint
@jobseeker_find_job.route("/jobseeker/find-jobs")
@verify_user
@is_email_verified
@is_qualification_done
@is_interests_done
@job_seeker_middleware
@is_skills_and_resume_done
def jobseeker_find_job_():
    return render_template("/pages/job_seeker/find_jobs.html")


@jobseeker_find_job.route("/api/jobseeker/get-jobs")
@verify_user
def jobseeker_find_job_api():
    try:
        db = get_db()
        search_term = request.args.get("search", "")

        # More robust parameter handling
        job_types = request.args.get("job_types", "")
        job_types_list = job_types.split(",") if job_types else []
        salary = request.args.get("salary", "")
        location = request.args.get("location", "")

        # Base query with proper parameter binding
        query = text("""
            SELECT j.*, e.*
            FROM jobs j 
            JOIN employers e ON j.employer_id = e.employer_id 
            WHERE j.status = 'active'
            AND (
                LOWER(j.title) LIKE :search 
                OR LOWER(j.description) LIKE :search
                OR LOWER(e.company_name) LIKE :search
            )
        """)

        params = {"search": f"%{search_term.lower()}%", "job_types": job_types}

        # Add job types filter if provided
        if job_types_list:
            query = text(str(query) + " AND FIND_IN_SET(j.employment_type, :job_types)")

        if salary:
            print("the given salary is:", salary)
            query = text(str(query) + " AND j.salary_range = :salary")
            params["salary"] = salary

        if location:
            query = text(str(query) + " AND LOWER(j.location) LIKE :location")
            params["location"] = f"%{location.lower()}%"

        try:
            result = db.execute_query(query, params)

            if not result["success"]:
                return jsonify(
                    {
                        "error": "Failed to fetch jobs",
                        "details": result.get("error", "Unknown database error"),
                    }
                ), 500

            jobs = result["output"]

            if not jobs:
                return "<div class='col-12 text-center py-5'><h4>No jobs found matching your criteria</h4><p>Try adjusting your search filters</p></div>"

            html_cards = []

            for job in jobs:
                if job["employment_type"] == "full_time":
                    job["employment_type"] = "Full Time"
                elif job["employment_type"] == "part_time":
                    job["employment_type"] = "Part Time"
                elif job["employment_type"] == "contract":
                    job["employment_type"] = "Contract"
                elif job["employment_type"] == "intern":
                    job["employment_type"] = "Intern"
                csrf_token = generate_csrf()

                card = f"""
                <div class="col-md-4 col-job-card">
                    <div class="job-card p-3 mb-3 d-flex flex-column">
                        <div class="d-flex align-items-center">
                            <img src="/assets/img/default_profile.jpg" alt="Company Logo" class="company-logo me-3">
                            <div>
                                <h5 class="company-name">{job["company_name"]}</h5>
                                <p class="job-type badge">{job["employment_type"]}</p>
                            </div>
                        </div>
                        <h4 class="job-title mt-3">{job["title"]}</h4>
                        
                        <p class="salary-range text-secondary">{job["salary_range"]}</p>
                        <p class="salary-range text-secondary">{job["employment_type"]}</p>
                        <p class="location"><i class="fas fa-map-marker-alt"></i> {job["location"]}</p>
                        <div class="mt-auto d-flex justify-content-between gap-2">
                            <form class="w-100" action='/api/jobseeker/apply' method='POST'>
                             <input type="hidden" name="csrf_token" value="{csrf_token}"/>
                                <input type="hidden" name='job_id' value='{job["job_id"]}'>
                                <button class="btn-primary w-100 rounded" type='submit'>Apply Now</button>
                            </form>
                             <form class="w-100" action='/api/jobseeker/save-job' method='POST'>
                             <input type="hidden" name="csrf_token" value="{csrf_token}"/>
                                <input type="hidden" name='job_id' value='{job["job_id"]}'>
                               <button class="btn-outline-secondary rounded w-100 h-100" type='submit'>Save</button>
                            </form>
                            
                        </div>
                    </div>
                </div>
                <script>  applyToAllForms(); </script>
                """
                html_cards.append(card)
               
            
            return "".join(html_cards)

        except Exception as db_error:
            print(f"Database Error: {str(db_error)}")
            return jsonify(
                {"error": "Database operation failed", "details": str(db_error)}
            ), 500

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Internal server error", "details": str(e)}), 500
