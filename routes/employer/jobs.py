from cgitb import html
from flask import Blueprint, render_template, session, jsonify, request
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
from utils.database import get_db
from sqlalchemy import text
from datetime import datetime
from middlewares.is_requirements_done import is_requirements_done
from utils.check_if_exists import check_column_exists
from flask_wtf.csrf import generate_csrf

# Create a Blueprint
jobs = Blueprint("jobs", __name__)


# Define your routes using the Blueprint
@jobs.route("/employer/jobs")
@verify_user
@is_email_verified
@is_requirements_done
def jobs_():
    logging.info("Rendering jobs page")
    return render_template("/pages/recruiter/jobs.html")


@jobs.route("/api/post-job", methods=["POST"])
def post_job_api():
    logging.info("Posting new job")
    try:
        db = get_db()

        query = text("""
            INSERT INTO jobs 
            (employer_id, title, description, location, salary_range, 
             employment_type, expires_at, status)
            VALUES 
            (:employer_id, :title, :description, :location, :salary_range,
             :employment_type, :expires_at, :status)
        """)

        # Get form data from request
        form_data = request.form

        result = db.execute_query(
            query,
            {
                "employer_id": session.get("user_id"),
                "title": form_data.get("title"),
                "description": form_data.get("description"),
                "location": form_data.get("location"),
                "salary_range": form_data.get("salary_range"),
                "employment_type": form_data.get("employment_type"),
                "expires_at": form_data.get("expires_at"),
                "status": "active",
            },
        )

        logging.info(f"Job posting result: {result}")
        if result["success"]:
            logging.info("Job posted successfully")
            return jsonify({"message": "Job posted successfully", "success": True}), 201
        else:
            logging.error(f"Job posting failed: {result['message']}")
            return jsonify(
                {"error": "Job posting failed", "details": result["message"]}
            ), 400

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"error": "Job posting failed", "details": str(e)}), 500


@jobs.route("/employer/post-job")
@verify_user
@is_email_verified
@is_requirements_done
def post_job_():
    logging.info("Rendering post job page")
    return render_template("/pages/recruiter/post_job.html")


@jobs.route("/api/employer/get-jobs")
@verify_user
@is_email_verified
@is_requirements_done
def get_jobs_api():
    logging.info("Fetching jobs")
    try:
        db = get_db()
        search_query = request.args.get("search", "")

        query = text("""
            SELECT 
                job_id,
                employer_id,
                title,
                description,
                location,
                salary_range,
                employment_type,
                posted_at,
                expires_at,
                status
            FROM jobs 
            WHERE employer_id = :employer_id
            ORDER BY posted_at DESC
        """)

        result = db.execute_query(query, {"employer_id": session.get("user_id")})
        logging.info(f"Search query: {search_query}")
        logging.info(f"SQL query: {query}")
        if result["success"]:
            logging.info("Jobs fetched successfully")
            return jsonify(result["output"]), 200
        else:
            logging.error(f"Failed to fetch jobs: {result['message']}")
            return jsonify(
                {"error": "Failed to fetch jobs", "details": result["message"]}
            ), 400

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"error": "Failed to fetch jobs", "details": str(e)}), 500


@jobs.route("/api/employer/get-job-cards")
@verify_user
@is_email_verified
@is_requirements_done
def get_job_cards():
    logging.info("Fetching job cards")
    try:
        db = get_db()

        # Get filter parameters
        status = request.args.get("status", "all")
        job_type = request.args.get("type", "all")
        sort_by = request.args.get("sort", "newest")
        search_query = request.args.get("search", "")
        approved_status_filter = request.args.get("statusFilter", "all")

        # Base query
        query = """
            SELECT 
                j.job_id,
                j.employer_id,
                j.title,
                j.description,
                j.location,
                j.salary_range,
                j.employment_type,
                j.posted_at,
                j.expires_at,
                j.status,
                j.approved,
                COUNT(a.application_id) as applicant_count
            FROM jobs j
            LEFT JOIN applications a ON j.job_id = a.job_id
            WHERE j.employer_id = :employer_id 
        """

        # Add filters
        if status != "all":
            query += " AND j.status = :status"
        if job_type != "all":
            query += " AND j.employment_type = :job_type"
        if search_query:
            query += " AND (j.title LIKE :search_query)"
        if approved_status_filter != "all":
            query += " AND j.approved = :approved_status_filter"

        query += " GROUP BY j.job_id"

        # Add sorting
        if sort_by == "newest":
            query += " ORDER BY j.posted_at DESC"
        elif sort_by == "oldest":
            query += " ORDER BY j.posted_at ASC"
        elif sort_by == "most_applications":
            query += " ORDER BY applicant_count DESC"
        elif sort_by == "alphabetical":
            query += " ORDER BY j.title ASC"

        # Prepare query parameters
        params = {"employer_id": session.get("user_id")}
        if status != "all":
            params["status"] = status.lower()
        if job_type != "all":
            params["job_type"] = job_type
        if search_query:
            params["search_query"] = f"%{search_query}%"
        if approved_status_filter != "all":
            params["approved_status_filter"] = int(approved_status_filter)

        result = db.execute_query(text(query), params)

        if result["success"]:
            jobs_html = ""
            for job in result["output"]:
                # Calculate days since posting
                posted_days = (datetime.now() - job["posted_at"]).days
                posted_text = f"{posted_days} days ago" if posted_days > 0 else "Today"
                #  print( job['employment_type'])
                if job["employment_type"] == "full_time":
                    job["employment_type"] = "Full Time"
                elif job["employment_type"] == "part_time":
                    job["employment_type"] = "Part Time"
                elif job["employment_type"] == "contract":
                    job["employment_type"] = "Contract"
                elif job["employment_type"] == "intern":
                    job["employment_type"] = "Intern"

                # Determine status badge color
                status_classes = {
                    "active": "bg-success",
                    "paused": "bg-warning",
                    "closed": "bg-danger",
                    "expired": "bg-danger",
                }

                expiry_date = job.get("expires_at")
                if expiry_date and expiry_date < datetime.now():
                    job["status"] = "expired"
                    sql = f"UPDATE jobs SET status = 'closed' WHERE job_id = {job['job_id']}"
                    try:
                        db.execute_query(text(sql),{"job_id": job["job_id"]})
                    except Exception as e:
                        logging.error('error updating expired status')

                status_class = status_classes.get(job["status"], "bg-secondary")
                approved_status = job["approved"]
              
                badge_icon = "question-circle"
                badge_text = "Unknown"
                badge_theme_color = "secondary"  # Bootstrap theme color
              
                if approved_status == 0:  # Pending
                   
                    badge_icon = "clock"
                    badge_text = "Pending Review"
                    badge_theme_color = "primary"

                elif approved_status == 1:  # Approved
                  
                    badge_icon = "check-circle"
                    badge_text = "Approved"
                    badge_theme_color = "success"

                elif approved_status == 3:  # Rejected
                  
                    badge_icon = "times-circle"
                    badge_text = "Rejected"
                    badge_theme_color = "danger"

                # Fallback for unknown status

                job_card = f"""
                <div class="col-12 col-md-6 col-lg-4 mb-4">
                    <div class="card job-card h-100">
                        <div class="card-body">
                            <div class="d-flex justify-content-between align-items-start mb-3">
                                <span class="badge {status_class} status-badge">{job["status"].title()}</span>
                                 <span class="badge bg-{badge_theme_color} bg-opacity-10 text-{badge_theme_color} status-badge">
                                 <i class="fas fa-{badge_icon} me-1"></i> {badge_text}
                    </span>
                                <div class="dropdown">
                                    <button class="btn btn-sm btn-link shadow-none text-muted p-0" type="button" data-bs-toggle="dropdown">
                                        <i class="fas fa-ellipsis-v"></i>
                                    </button>
                                    <ul class="dropdown-menu dropdown-menu-end">
                                        <li><a class="dropdown-item" href="/employer/edit-job/{job["job_id"]}"><i class="fas fa-edit me-2"></i>Edit</a></li>
                                        <li><a class="dropdown-item text-danger" href="#" onclick="deleteJob({job["job_id"]})"><i class="fas fa-trash me-2"></i>Delete</a></li>
                                    </ul>
                                </div>
                            </div>
                            <h5 class="card-title">{job["title"]}</h5>
                            <p class="card-text text-muted mb-2"><i class="fas fa-briefcase me-2"></i>{job["employment_type"]}</p>
                            <p class="card-text text-muted mb-2"><i class="fas fa-map-marker-alt me-2"></i>{job["location"]}</p>
                            <p class="card-text text-muted mb-3"><i class="fas fa-clock me-2"></i>Posted {posted_text}</p>
                            <div class="d-flex flex-wrap justify-content-between align-items-center">
                                <span class="text-primary mb-2 mb-sm-0"><i class="fas fa-users me-1"></i> {job["applicant_count"]} applicants</span>
                                <a href="/employer/job/{job["job_id"]}" class="btn btn-sm btn-outline-primary">View Details</a>
                            </div>
                        </div>
                    </div>
                </div>
                """
                jobs_html += job_card

            logging.info("Job cards fetched successfully")
            return jobs_html
        else:
            logging.error(f"Failed to fetch job cards: {result['message']}")
            return """
                <div class="col-12 text-center py-5">
                    <div class="no-data-found">
                        <i class="fas fa-folder-open fa-3x text-muted mb-3"></i>
                        <h5 class="text-muted">No Jobs Found</h5>
                        <p class="text-muted">You haven't posted any jobs yet.</p>
                        <a href="/employer/post-job" class="btn btn-primary mt-2">
                            <i class="fas fa-plus me-2"></i>Post a New Job
                        </a>
                    </div>
                </div>
            """

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Failed to fetch jobs", "details": str(e)}), 500




@jobs.route("/api/employer/get-job-cards-v1", methods=["GET"])
def get_job_cards_v1():
    """
    Retrieve active job postings and related statistics for an employer.

    This function queries the database to gather various statistics and
    information about an employer's active job postings, including the number
    of total candidates, total jobs posted, active job listings, successful
    hires, and company profile details. Additionally, it fetches contact
    information, job statistics, chart data on application statuses, and
    recent applications.

    Parameters:
        id (int): The employer's ID to query data for.

    Returns:
        JSON response containing success status and the retrieved data if
        successful, otherwise a JSON response with an error message and
        HTTP status 500.
    """

    db = get_db()
    employer_id = request.args.get("employer_id") or request.form.get("employer_id") # Using static user ID as requested
    
    query = text("""
        WITH dashboard_summary AS (
            SELECT COUNT(DISTINCT a.seeker_id) AS total_candidates
            FROM applications a
            JOIN jobs j ON a.job_id = j.job_id
            WHERE j.employer_id = :employer_id
        ),
        total_job_posted AS (
            SELECT COUNT(*) AS total_job_posted
            FROM jobs
            WHERE employer_id = :employer_id
        ),
        active_job_listings AS (
            SELECT COUNT(*) AS active_job_listings
            FROM jobs
            WHERE employer_id = :employer_id AND status = 'active'
        ),
        successful_hires AS (
            SELECT COUNT(*) AS successful_hires
            FROM applications a
            JOIN jobs j ON a.job_id = j.job_id
            WHERE j.employer_id = :employer_id AND a.status = 'shortlisted'
        ),
        company_profile AS (
            SELECT company_name, logo_url, industry, company_size, website, field
            FROM employers
            WHERE employer_id = :employer_id
        ),
        active_job_postings AS (
            SELECT job_id, title, posted_at, status
            FROM jobs
            WHERE employer_id = :employer_id AND status = 'active'
            ORDER BY posted_at DESC
        ),
        contact_information AS (
            SELECT email, website
            FROM employers
            WHERE employer_id = :employer_id
        ),
        job_statistics AS (
            SELECT 
                (SELECT COUNT(*) FROM jobs WHERE employer_id = :employer_id) AS total_jobs_posted,
                (SELECT COUNT(*) FROM jobs WHERE employer_id = :employer_id AND status = 'active') AS currently_active_jobs
        ),
        chart_data AS (
            SELECT a.status, COUNT(*) AS count
            FROM applications a
            JOIN jobs j ON a.job_id = j.job_id
            WHERE j.employer_id = :employer_id
            GROUP BY a.status
        ),
        recent_applications AS (
            SELECT js.first_name, js.last_name, j.title AS position, a.status
            FROM applications a
            JOIN jobs j ON a.job_id = j.job_id
            JOIN job_seekers js ON a.seeker_id = js.seeker_id
            WHERE j.employer_id = :employer_id
            ORDER BY a.applied_at DESC
            LIMIT 10
        )
        SELECT 
            (SELECT total_candidates FROM dashboard_summary) AS total_candidates,
            (SELECT total_job_posted FROM total_job_posted) AS total_job_posted,
            (SELECT active_job_listings FROM active_job_listings) AS active_job_listings,
            (SELECT successful_hires FROM successful_hires) AS successful_hires,
            (SELECT company_name FROM company_profile) AS company_name,
            (SELECT field FROM company_profile) AS field,
            (SELECT logo_url FROM company_profile) AS logo_url,
            (SELECT industry FROM company_profile) AS industry,
            (SELECT company_size FROM company_profile) AS company_size,
            (SELECT website FROM company_profile) AS company_website,
            (SELECT GROUP_CONCAT(CONCAT_WS('||||', job_id, title, posted_at, status) SEPARATOR ';;;;') FROM active_job_postings) AS active_job_postings,
            (SELECT email FROM contact_information) AS email,
            (SELECT website FROM contact_information) AS contact_website,
            (SELECT total_jobs_posted FROM job_statistics) AS total_jobs_posted,
            (SELECT currently_active_jobs FROM job_statistics) AS currently_active_jobs,
            (SELECT GROUP_CONCAT(CONCAT_WS('||||', status, count) SEPARATOR ';;;;') FROM chart_data) AS chart_data,
            (SELECT GROUP_CONCAT(CONCAT_WS('||||', first_name, last_name, position, status) SEPARATOR ';;;;') FROM recent_applications) AS recent_applications
    """)
    
    result = db.execute_query(query, {"employer_id": employer_id})
    
    if result["success"]:
       
        # Process active job postings data
        if not result["output"]: # Handle case where query returns no data for the employer_id
            # Return a structure with default/empty values if appropriate for your frontend
            return jsonify({
                'success': True,
                'data': [{
                    'total_candidates': 0,
                    'total_job_posted': 0,
                    'active_job_listings': 0,
                    'successful_hires': 0,
                    'company_name': None,
                    'field': None,
                    'logo_url': None,
                    'industry': None,
                    'company_size': None,
                    'company_website': None,
                    'active_job_postings': [],
                    'email': None,
                    'contact_website': None,
                    'currently_active_jobs': 0,
                    'chart_data': [],
                    'recent_applications': []
                }]
            })

        data_row = result["output"][0]

        active_postings_str = data_row.get('active_job_postings')
        processed_postings = []
        if active_postings_str:
            job_entries = active_postings_str.split(';;;;')
            for entry in job_entries:
                if not entry: continue
                parts = entry.split('||||')
                if len(parts) == 4:
                    processed_postings.append({
                        'job_id': parts[0],
                        'title': parts[1],
                        'posted_at': parts[2],
                        'status': parts[3]
                    })
                else:
                    print(f"Warning: Malformed active_job_posting entry: {entry}") # Add logging
        data_row['active_job_postings'] = processed_postings
               
        # Process chart data
        chart_data_str = data_row.get('chart_data')
        processed_chart_data = []
        if chart_data_str:
            chart_entries = chart_data_str.split(';;;;')
            for entry in chart_entries:
                if not entry: continue
                parts = entry.split('||||')
                if len(parts) == 2:
                    processed_chart_data.append({
                        'status': parts[0],
                        'count': int(parts[1]) if parts[1].isdigit() else parts[1]
                    })
                else:
                    print(f"Warning: Malformed chart_data entry: {entry}") # Add logging
        data_row['chart_data'] = processed_chart_data

        # Process recent applications data
        recent_apps_str = data_row.get('recent_applications')
        processed_recent_apps = []
        if recent_apps_str:
            app_entries = recent_apps_str.split(';;;;')
            for entry in app_entries:
                if not entry: continue
                parts = entry.split('||||')
                if len(parts) == 4:
                    processed_recent_apps.append({
                        'first_name': parts[0],
                        'last_name': parts[1],
                        'position': parts[2],
                        'status': parts[3]
                    })
                else:
                    print(f"Warning: Malformed recent_application entry: {entry}") # Add logging
        data_row['recent_applications'] = processed_recent_apps

        print(result["output"])
        return jsonify({
            'success': True,
            'data': result["output"]
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Failed to fetch active job postings'
        }), 500


@jobs.route("/employer/edit-job/<int:job_id>")
@verify_user
@is_email_verified
@is_requirements_done
def edit_job_1(job_id):
    from flask import Response

    if request.method == "GET":
        if job_id:
            logging.info(f"Editing job with ID: {job_id}")
            db = get_db()
            is_id_exists = check_column_exists("jobs", "job_id", job_id)

            is_own_by_emp = db.execute_query(
                text(
                    "SELECT * FROM jobs WHERE job_id = :job_id AND employer_id = :employer_id"
                ),
                {"job_id": job_id, "employer_id": session.get("user_id")},
            )
            if is_own_by_emp["success"] and not is_own_by_emp["output"]:
                logging.warning(f"Job ID {job_id} does not belong to the current user")
                return render_template("/pages/job_not_found.html")
            if is_id_exists:
                logging.info("Job ID exists")
                result = db.execute_query(
                    text("SELECT * FROM jobs WHERE job_id = :job_id"),
                    {"job_id": job_id},
                )
                if result["success"]:
                    job = result["output"][0]
                    title = job["title"]
                    description = job["description"]
                    location = job["location"]
                    salary_range = job["salary_range"]
                    employment_type = job["employment_type"]
                    expires_at = job["expires_at"]
                    status = job["status"]
                    posted_at = job["posted_at"]

                    logging.info(f"Job {job_id} details retrieved successfully")
                    return render_template(
                        "/pages/recruiter/edit_job.html",
                        title=title,
                        description=description,
                        location=location,
                        salary_range=salary_range,
                        employment_type=employment_type,
                        expires_at=expires_at,
                        status=status,
                        id=job_id,
                        posted_at=posted_at,
                    )
            logging.error(f"Failed to retrieve job {job_id} details")
            return render_template("/pages/job_not_found.html")


@jobs.route("/employer/api/edit-job", methods=["POST"])
@verify_user
@is_email_verified
@is_requirements_done
def edit_job_():
    try:
        db = get_db()

        form_data = request.form
        logging.info(f"Editing job with ID: {form_data.get('id')}")

        query = text("""
                UPDATE jobs
                SET title = :title, description = :description, location = :location,
                    salary_range = :salary_range, employment_type = :employment_type,
                    expires_at = :expires_at, status = :status
                WHERE job_id = :job_id
            """)
        result = db.execute_query(
            query,
            {
                "job_id": form_data.get("id"),
                "title": form_data.get("title"),
                "description": form_data.get("description"),
                "location": form_data.get("location"),
                "salary_range": form_data.get("salary_range"),
                "employment_type": form_data.get("employment_type"),
                "expires_at": form_data.get("expires_at"),
                "status": form_data.get("status"),
            },
        )
        if result["success"]:
            logging.info(f"Job {form_data.get('id')} updated successfully")
            return jsonify(
                {"message": "Job updated successfully", "success": True}
            ), 200
        else:
            logging.error(f"Job update failed: {result['message']}")
            return jsonify(
                {"error": "Failed to update job", "details": result["message"]}
            ), 400
    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return jsonify({"error": "Failed to update job", "details": str(e)}), 500


@jobs.route("/employer/api/delete-job", methods=["POST"])
@verify_user
@is_email_verified
@is_requirements_done
def delete_job_():
    logging.info("Delete job route called")
    try:
        db = get_db()
        form_data = request.form
        job_id = form_data.get("id")

        if not job_id:
            logging.error("Job ID is required but not provided")
            return jsonify({"error": "Job ID is required"}), 400

        logging.info(f"Attempting to delete job with ID: {job_id}")
        query = text(
            "DELETE FROM jobs WHERE job_id = :job_id AND employer_id = :employer_id"
        )
        result = db.execute_query(
            query,
            {
                "job_id": job_id,
                "employer_id": session.get("user_id"),
            },
        )

        if result["success"]:
            logging.info(f"Job {job_id} deleted successfully")
            return jsonify(
                {"message": "Job deleted successfully", "success": True}
            ), 200
        else:
            logging.error(f"Job deletion failed for ID {job_id}: {result['message']}")
            logging.debug(f"Result details: {result}")
            return jsonify(
                {"error": "Failed to delete job", "details": result["message"]}
            ), 400

    except Exception as e:
        logging.error(f"Error while deleting job ID {job_id}: {str(e)}")
        return jsonify({"error": "Failed to delete job", "details": str(e)}), 500
