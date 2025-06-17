from flask import Blueprint, render_template, request, jsonify
from middlewares.verify_user import verify_user
from utils.database import get_db
from sqlalchemy import text
import logging

# Create Blueprint
job_approval = Blueprint("job_approval", __name__)

def _generate_no_jobs_found_html():
    """Generates HTML for the 'no jobs found' message."""
    return """
    <div class="row no-results text-center py-5">
        <div class="col-12">
            <i class="fas fa-search fa-3x mb-3 text-muted"></i>
            <h4>No jobs found</h4>
            <p class="text-muted">Try adjusting your search or filter criteria.</p>
        </div>
    </div>
    """

@job_approval.route("/admin/job_approval")
@job_approval.route("/admin/job_approval.html")
@verify_user
def job_approval_view():
    """Renders the job approval page"""
    return render_template("/pages/admin/job_approval.html")

@job_approval.route("/admin/get_jobs_by_status")
@verify_user
def get_jobs_by_status():
    """Fetch jobs by approval status (0 = pending, 1 = approved)"""
    # This route is kept for potential other uses, but the main page will use search_jobs.
    db = get_db()
    status = request.args.get("status")  # 0 or 1
    logging.info(f"Fetching jobs with approved={status}")
    
    params = {}
    base_query = """
        SELECT j.*, e.company_name
        FROM jobs j
        JOIN employers e ON j.employer_id = e.employer_id
    """
    if status in ("0", "1"):
        query = base_query + " WHERE j.approved = :status"
        params["status"] = status
    elif status and status.lower() == "all":
        query = base_query
    else: # Default to all or handle invalid status as no results
        query = base_query # Or return an error/empty if status is present but invalid
        logging.warning(f"Invalid or no status provided to get_jobs_by_status: {status}. Fetching all.")

    result = db.execute_query(text(query), params)
    
    if result["success"]:
        html = ""
        if not result["output"]:
            html = _generate_no_jobs_found_html()
        else:
            for row in result["output"]:
                html += generate_job_card(row)
        return jsonify({"success": True, "html": html})
    else:
        logging.error(f"Failed to fetch jobs: {result}")
        return jsonify({"success": False, "error": "Database error"})
    
@job_approval.route("/admin/search_job_approval", methods=["POST"])
@verify_user
def search_jobs():
    """Search jobs by title or approval status"""
    db = get_db()

    data = request.get_json() or request.form
    search_query = data.get("search_query") or ""
    status_filter = data.get("status_filter")
    type_filter = data.get("type_filter")

    logging.debug(f"Received data: {data}")

    logging.info(f"Search initiated with query: '{search_query}', status filter: '{status_filter}', type filter: '{type_filter}'")

    query = """
        SELECT j.*, e.company_name
        FROM jobs j
        JOIN employers e ON j.employer_id = e.employer_id
        WHERE 1=1
    """
    params = {}

    if status_filter and status_filter.lower() != "all" and status_filter in ("0", "1", "3"):
        query += " AND j.approved = :status"
        params["status"] = status_filter
    
    if type_filter and type_filter.lower() != "all":
        query += " AND j.employment_type = :type"
        params["type"] = type_filter
    
    if search_query:
        query += " AND LOWER(j.title) LIKE LOWER(:title)" # Case-insensitive search
        params["title"] = f"%{search_query.lower()}%"

    logging.debug(f"Executing query: {query} with params: {params}")

    result = db.execute_query(text(query), params)
    
    if result["success"]:
        if not result["output"]:
            html = _generate_no_jobs_found_html()
            logging.info("Search successful, 0 results found")
        else:
            html = "".join(generate_job_card(row) for row in result["output"])
            logging.info(f"Search successful, {len(result['output'])} results found")
        
        return jsonify({"success": True, "html": html})
    else:
        logging.error(f"Search failed due to a database error {result}")
        return jsonify({"success": False, "error": "Search failed"})
    
@job_approval.route("/admin/update_job_status", methods=["POST"])
@verify_user
def update_job_status():
    """Approve or reject a job"""
    data = request.get_json() or request.form
    job_id = data.get("job_id")
    approved = data.get("status")  # "approve" or "reject"
    admin_notes = data.get("admin_notes", "").strip()

    logging.info(f"Updating job {job_id} with status {approved} and admin notes {admin_notes}")

    if not job_id:
        logging.warning("Missing job ID")
        return jsonify({"success": False, "error": "Missing job ID"}), 400
    
    if approved not in ("approve", "reject"):
        logging.warning(f"Invalid status {approved}")
        return jsonify({"success": False, "error": "Invalid status"}), 400

    try:
        if approved == "approve":
            approved_flag = 1   # Approved
        elif approved == "reject": # This is the only other valid option due to check above
            approved_flag = 3   # Rejected
        else: # Should not be reached
            approved_flag = 0   # Default to Pending/Unreviewed
        logging.info(f"Updating job {job_id} with status {approved_flag}")
        query = """
            UPDATE jobs
            SET approved = :approved
            WHERE job_id = :job_id
        """
        db = get_db()
        result = db.execute_query(
            text(query),
            {
                "approved": approved_flag,
                "job_id": job_id
            }
        )
        if result["success"]:
            action_taken = "unknown"
            if approved_flag == 1:
                action_taken = "approved"
            elif approved_flag == 3:
                action_taken = "rejected"
            logging.info(f"Job {job_id} {action_taken}")
            return jsonify({
                "success": True,
                "message": f"Job {job_id} {action_taken}",
                "data": {"job_id": job_id, "approved": approved_flag}
            })
        else:
            logging.error(f"Update failed for job {job_id} {result}")
            return jsonify({"success": False, "error": "Update failed"})
    except Exception as e:
        logging.error(f"Error updating job status for job {job_id}: {e}")
        return jsonify({"success": False, "error": str(e)})
    

def generate_job_card(row):
    """Generate HTML for a job card based on approval status"""
    approved_status = row["approved"] # Integer: 0 for pending, 1 for approved, 3 for rejected

    status_class = "unknown"
    badge_icon = "question-circle"
    badge_text = "Unknown"
    badge_theme_color = "secondary" # Bootstrap theme color
    action_buttons = ""

    if approved_status == 0:  # Pending
        status_class = "pending"
        badge_icon = "clock"
        badge_text = "Pending Review"
        badge_theme_color = "primary" 
        action_buttons = f"""
            <button class="btn btn-success btn-sm action-btn" onclick="approveJob(this)">
                <i class="fas fa-check me-1"></i> Approve
            </button>
            <button class="btn btn-outline-danger btn-sm action-btn" onclick="rejectJob(this)">
                <i class="fas fa-times me-1"></i> Reject
            </button>
        """
    elif approved_status == 1:  # Approved
        status_class = "approved"
        badge_icon = "check-circle"
        badge_text = "Approved"
        badge_theme_color = "success"
        action_buttons = f"""
            <button class="btn btn-success btn-sm action-btn disabled" aria-disabled="true">
                <i class="fas fa-check me-1"></i> Approved
            </button>
        """
    elif approved_status == 3:  # Rejected
        status_class = "rejected"
        badge_icon = "times-circle"
        badge_text = "Rejected"
        badge_theme_color = "danger"
        action_buttons = f"""
            <button class="btn btn-danger btn-sm action-btn disabled" aria-disabled="true">
                <i class="fas fa-times me-1"></i> Rejected
            </button>
        """
    else: # Fallback for unknown status
        action_buttons = "<p class='text-muted small'>Status action undefined</p>"

    return f"""
    <div class="col-12 col-md-6 col-lg-4 mb-4 job-item" 
         data-status="{status_class}" 
         data-title="{row['title']}"> 
        <div class="card job-card {status_class} h-100 shadow-sm">
            <div class="card-body d-flex flex-column">
                <div class="d-flex justify-content-between align-items-start mb-3">
                    <span class="badge bg-{badge_theme_color} bg-opacity-10 text-{badge_theme_color} status-badge">
                        <i class="fas fa-{badge_icon} me-1"></i> {badge_text}
                    </span>
                    <small class="text-muted">ID: {row['job_id']}</small>
                </div>
                <h5 class="card-title mb-3">{row['title']}</h5>
                <input type="hidden" name="job_id" value="{row['job_id']}">
                <div class="job-meta mb-3">
                    <div class="d-flex align-items-center mb-2">
                        <i class="fas fa-briefcase me-2"></i>
                        <span>{row['employment_type'].replace('_', ' ').title()}</span>
                    </div>
                    <div class="d-flex align-items-center mb-2">
                        <i class="fas fa-map-marker-alt me-2"></i>
                        <span>{row['location']}</span>
                    </div>
                    <div class="d-flex align-items-center">
                        <i class="fas fa-clock me-2"></i>
                        <span>Posted {row['posted_at']}</span>
                    </div>
                </div>
                <div class="mt-auto d-flex justify-content-between align-items-center">
                    <span class="applicant-count">
                        <i class="fas fa-users me-1"></i> {row.get('applicant_count', 0)} applicants
                    </span>
                    <div class="d-flex gap-2">
                        {action_buttons}
                    </div>
                </div>
            </div>
        </div>
    </div>
    """
