from cgitb import html
from flask import Blueprint, render_template, session, jsonify, request
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
from utils.database import get_db
from sqlalchemy import text
from datetime import datetime
from middlewares.is_requirements_done import is_requirements_done
from utils.check_if_exists import check_column_exists
import logging
# Create a Blueprint
jobs = Blueprint("jobs", __name__)


# Define your routes using the Blueprint
@jobs.route("/employer/jobs")
@verify_user
@is_email_verified
@is_requirements_done
def jobs_():
    return render_template("/pages/recruiter/jobs.html")


@jobs.route("/api/post-job", methods=["POST"])
def post_job_api():
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

        print("emplymernt type:", form_data.get("employment_type"))

        if result["success"]:
            logging.debug("Job posted successfully")
            return jsonify({"message": "Job posted successfully", "success": True}), 201
        else:
            print(f"Job posting failed: {result['message']}")
            return jsonify(
                {"error": "Job posting failed", "details": result["message"]}
            ), 400

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Job posting failed", "details": str(e)}), 500


@jobs.route("/employer/post-job")
@verify_user
@is_email_verified
@is_requirements_done
def post_job_():
    return render_template("/pages/recruiter/post_job.html")


@jobs.route("/api/employer/get-jobs")
@verify_user
@is_email_verified
@is_requirements_done
def get_jobs_api():
    try:
        db = get_db()

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

        if result["success"]:
            return jsonify(result["output"]), 200
        else:
            return jsonify(
                {"error": "Failed to fetch jobs", "details": result["message"]}
            ), 400

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Failed to fetch jobs", "details": str(e)}), 500


@jobs.route("/api/employer/get-job-cards")
@verify_user
@is_email_verified
@is_requirements_done
def get_job_cards():
    try:
        db = get_db()

        # Get filter parameters
        status = request.args.get("status", "all")
        job_type = request.args.get("type", "all")
        sort_by = request.args.get("sort", "newest")
        search_query = request.args.get("search", "")

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
            query += (
                " AND (j.title LIKE :search_query OR j.description LIKE :search_query)"
            )

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
                status_class = (
                    "bg-success" if job["status"] == "active" else "bg-secondary"
                )

                job_card = f"""
                <div class="col-12 col-md-6 col-lg-4 mb-4">
                    <div class="card job-card h-100">
                        <div class="card-body">
                            <div class="d-flex justify-content-between align-items-start mb-3">
                                <span class="badge {status_class} status-badge">{job["status"].title()}</span>
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

            return jobs_html
        else:
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


@jobs.route("/api/employer/get-job-cards-v1")
def get_job_cards_public():
    try:
        db = get_db()

        # Get filter parameters
        status = request.args.get("status", "all")
        job_type = request.args.get("type", "all")
        sort_by = request.args.get("sort", "newest")

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
        params = {"employer_id": request.args.get("employer_id")}
        if status != "all":
            params["status"] = status.lower()
        if job_type != "all":
            params["job_type"] = job_type

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
                status_class = (
                    "bg-success" if job["status"] == "active" else "bg-secondary"
                )

                job_card = f"""
                <div class="col-12 col-md-6 col-lg-4 mb-4">
                    <div class="card job-card h-100">
                        <div class="card-body">
                            <div class="d-flex justify-content-between align-items-start mb-3">
                                <span class="badge {status_class} status-badge">{job["status"].title()}</span>
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

            return jobs_html
        else:
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


@jobs.route("/employer/edit-job/<int:job_id>")
@verify_user
@is_email_verified
@is_requirements_done
def edit_job_1(job_id):
    from flask import Response

    if request.method == "GET":
        if job_id:
            print(f"Editing job with ID: {job_id}")
            db = get_db()
            is_id_exists = check_column_exists("jobs", "job_id", job_id)

            is_own_by_emp = db.execute_query(
                text(
                    "SELECT * FROM jobs WHERE job_id = :job_id AND employer_id = :employer_id"
                ),
                {"job_id": job_id, "employer_id": session.get("user_id")},
            )
            if is_own_by_emp["success"] and not is_own_by_emp["output"]:
                return render_template("/pages/job_not_found.html")
            if is_id_exists:
                print("Job ID exists")
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
            return render_template("/pages/job_not_found.html")


@jobs.route("/employer/api/edit-job", methods=["POST"])
@verify_user
@is_email_verified
@is_requirements_done
def edit_job_():
    try:
        db = get_db()

        form_data = request.form
        print(form_data)
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
            print("Job updated successfully", result, form_data)
            return jsonify(
                {"message": "Job updated successfully", "success": True}
            ), 200
        else:
            print(f"Job update failed: {result['message']}")
            return jsonify(
                {"error": "Failed to update job", "details": result["message"]}
            ), 400
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Failed to update job", "details": str(e)}), 500


@jobs.route("/employer/api/delete-job", methods=["POST"])
@verify_user
@is_email_verified
@is_requirements_done
def delete_job_():
    print("delete_job_ route called")
    try:
        db = get_db()
        form_data = request.form
        job_id = form_data.get("id")

        if not job_id:
            return jsonify({"error": "Job ID is required"}), 400

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
            print("Job deleted successfully")
            return jsonify(
                {"message": "Job deleted successfully", "success": True}
            ), 200
        else:
            print(f"Job deletion failed: {result['message']}")
            print(f"Result details: {result}")
            return jsonify(
                {"error": "Failed to delete job", "details": result["message"]}
            ), 400

    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "Failed to delete job", "details": str(e)}), 500
