from flask import Blueprint, render_template, request, jsonify
from middlewares.verify_user import verify_user
from utils.database import get_db
from sqlalchemy import text
from datetime import datetime
# Create a Blueprint
recruiter_approval = Blueprint("recruiter_approval", __name__)


@recruiter_approval.route("/admin/recruiter_approval")
@recruiter_approval.route("/admin/recruiter_approval.html")
@verify_user
def recruiter_approval_view():
    """
    Renders the recruiter approval page for the admin.

    This view is protected by a user verification middleware to ensure
    that only verified users can access the recruiter approval page.

    Returns:
        A rendered HTML template for the recruiter approval page.
    """

    return render_template("/pages/admin/recruiter_approval.html")


@recruiter_approval.route("/admin/get_recruiter_by_status")
@verify_user
def get_recruiter():
    """
    Returns a list of employers matching the given verification status.

    The list of employers will contain their verification status.

    Args:
        status (str): The verification status to filter by.

    Returns:
        A JSON response containing the list of employers. The response will have
        a "success" key set to True on success, or False on failure. If the request
        was successful, the response will also contain a "data" key with the list
        of employers. If the request failed, the response will contain an "error"
        key with a description of the error.

    Raises:
        400: If the required "status" parameter is missing.
    """
   

    db = get_db()
    form = request.form
    status = form.get("status") or request.args.get("status")
    logging.info(f"Requesting recruiters with status {status}")

    if not status:
        logging.info("Requesting all recruiters without filter")
        result = db.execute_query(
            text("""
                SELECT 
                    e.*,
                    COALESCE(ev.status, 'pending') AS verification_status
                FROM employers e
                LEFT JOIN employer_verification ev ON e.employer_id = ev.employer_id
            """)
        )
    else:
        result = db.execute_query(
            text("""
                SELECT 
                    e.*,
                    COALESCE(ev.status, 'pending') AS verification_status
                FROM employers e
                LEFT JOIN employer_verification ev ON e.employer_id = ev.employer_id
                WHERE ev.status = :status
            """),
            {
                "status": status
            }
        )

    if result["success"]:
        logging.info(f"Successfully retrieved {len(result['output'])} recruiters with status {status}")
        html = ""
        for row in result["output"]:
            html += f"""
            <div class="col-12 col-md-6 col-lg-4 mb-4 recruiter-item" data-status="{row['verification_status']}" data-company_name="{row['company_name']}">
                <div class="card recruiter-card {row['verification_status']} h-100 shadow-sm">
                    <div class="card-body d-flex flex-column">
                        <div class="d-flex justify-content-between align-items-start mb-3">
                            <span class="badge bg-{row['verification_status']} bg-opacity-10 text-{row['verification_status']} status-badge">
                                <i class="fas fa-{row['verification_status'] == 'pending' and 'clock' or 'check-circle'} me-1"></i> {row['verification_status'].capitalize()} Review
                            </span>
                            <small class="text-muted">ID: {row['employer_id']}</small>
                        </div>
                        
                        <h5 class="card-title mb-2">{row['company_name']}</h5>
                        <p class="text-muted mb-3"><i class="fas fa-envelope me-1"></i> {row['email']}</p>
                        
                        <div class="job-meta mb-3">
                            <div class="d-flex align-items-center mb-2">
                                <i class="fas fa-user-tie me-2"></i>
                                <span>Contact: nonevar</span>
                            </div>
                            <div class="d-flex align-items-center mb-2">
                                <i class="fas fa-phone me-2"></i>
                                <span>+1 nonvar</span>
                            </div>
                            <div class="d-flex align-items-center">
                                <i class="fas fa-clock me-2"></i>
                                <span>Registered nonevar ago</span>
                            </div>
                        </div>
                        
                        <div class="mt-auto">
                            <a href="#viewRequirements" class="d-block mb-2 text-primary" 
                               data-bs-toggle="modal" data-bs-target="#requirementsModal"
                               onclick="loadRequirements('{row['employer_id']}')">
                                <i class="fas fa-file-alt me-1"></i> View Requirements
                            </a>
                            <div class="d-flex gap-2">
                                <button class="btn btn-success btn-sm action-btn" onclick="approveRecruiter(this)">
                                    <i class="fas fa-check me-1"></i> Approve
                                </button>
                                <button class="btn btn-outline-danger btn-sm action-btn" onclick="rejectRecruiter(this)">
                                    <i class="fas fa-times me-1"></i> Reject
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """
        if not result["output"]:
            logging.warn("No recruiters found")
            html = """"  <div class="row no-results text-center py-5" id="noResults" style="display: none;">
                <div class="col-12">
                    <i class="fas fa-search fa-3x mb-3 text-muted"></i>
                    <h4>No recruiters found</h4>
                    <p class="text-muted">Try adjusting your search or filter criteria</p>
                </div>
            </div>"""
        return jsonify({"success": True, "data": result["output"], "html": html}), 200
    else:
        logging.error(f"Failed to retrieve recruiters with status {status}: {result}")
        return jsonify({"success": False, "error": result}), 500


@recruiter_approval.route("/admin/search_recruiter_approval")
@verify_user
def search_recruiter():
    """
    Returns a list of employers filtered by verification status and/or company name.

    Args:
        status (str): The verification status to filter by.
        company_name (str): Partial match on company name.

    Returns:
        A JSON response containing the list of employers or error message.
    """
    db = get_db()
    form = request.form
    status = form.get("status") or request.args.get("status")
    company_name = form.get("company_name") or request.args.get("company_name")

    logging.info(f"Requesting recruiters with status={status}, company_name={company_name}")

    base_query = """
        SELECT 
            e.*,
            COALESCE(ev.status, 'pending') AS verification_status
        FROM employers e
        LEFT JOIN employer_verification ev ON e.employer_id = ev.employer_id
    """

    where_clauses = []
    params = {}

    if status and status != "all":
        where_clauses.append("ev.status = :status")
        params["status"] = status

    if company_name and company_name != "":
        where_clauses.append("e.company_name LIKE :company_name")
        params["company_name"] = f"%{company_name}%"

    if where_clauses:
        base_query += " WHERE " + " OR ".join(where_clauses)

    result = db.execute_query(text(base_query), params)

    if result["success"]:
        logging.info(f"Successfully retrieved {len(result['output'])} recruiters")
        html = ""
        for row in result["output"]:
            parentDiv = ""
            badge = ""
            button = ""
            if row['verification_status'] == 'rejected':
                parentDiv = 'parentDiv.setAttribute("data-status", "rejected");'
                badge = """
                    <span class="badge bg-danger bg-opacity-10 text-danger status-badge">
                        <i class="fas fa-times-circle me-1"></i> Rejected
                    </span>
                """
                button = """
                    <button class="btn btn-danger btn-sm action-btn disabled">
                        <i class="fas fa-times me-1"></i> Rejected
                    </button>
                """
            elif row['verification_status'] == 'approved':
                badge = f"""
                    <span class="badge bg-success bg-opacity-10 text-success status-badge">
                        <i class="fas fa-check-circle me-1"></i> Approved
                    </span>
                """
                button = f"""
                    <button class="btn btn-success btn-sm action-btn" disabled>
                        <i class="fas fa-check me-1"></i> Approved
                    </button>
                """
            else:
                badge = f"""
                    <span class="badge bg-{row['verification_status']} bg-opacity-10 text-{row['verification_status']} status-badge">
                        <i class="fas fa-{row['verification_status'] == 'pending' and 'clock' or 'check-circle'} me-1"></i> {row['verification_status'].capitalize()} Review
                    </span>
                """
                button = f"""
                     <button class="btn btn-success btn-sm action-btn" onclick="approveRecruiter(this, {row['employer_id']})">
                                    <i class="fas fa-check me-1"></i> Approve
                                </button>
                                <button class="btn btn-outline-danger btn-sm action-btn" onclick="rejectRecruiter(this,{row['employer_id']})">
                                    <i class="fas fa-times me-1"></i> Reject
                                </button>
                """

            html += f"""
            <div class="col-12 col-md-6 col-lg-4 mb-4 recruiter-item" data-status="{row['verification_status']}" data-company_name="{row['company_name']}">
                <div class="card recruiter-card {row['verification_status']} h-100 shadow-sm" {parentDiv}>
                    <div class="card-body d-flex flex-column">
                        <div class="d-flex justify-content-between align-items-start mb-3">
                            {badge}
                            <small class="text-muted">ID: {row['employer_id']}</small>
                        </div>
                        
                        <input type="hidden" name="employer_id" value="{row['employer_id']}">

                        <h5 class="card-title mb-2">{row['company_name']}</h5>
                        <p class="text-muted mb-3"><i class="fas fa-envelope me-1"></i> {row['email']}</p>

                        <div class="job-meta mb-3">
                            <div class="d-flex align-items-center mb-2">
                                <i class="fas fa-user-tie me-2"></i>
                                <span>Contact: nonevar</span>
                            </div>
                            <div class="d-flex align-items-center mb-2">
                                <i class="fas fa-phone me-2"></i>
                                <span>+1 nonvar</span>
                            </div>
                            <div class="d-flex align-items-center">
                                <i class="fas fa-clock me-2"></i>
                                <span>Registered nonevar ago</span>
                            </div>
                        </div>

                        <div class="mt-auto">
                            <a href="#viewRequirements" class="d-block mb-2 text-primary" 
                               data-bs-toggle="modal" data-bs-target="#requirementsModal"
                               onclick="loadRequirements('{row['employer_id']}')">
                                <i class="fas fa-file-alt me-1"></i> View Requirements
                            </a>
                            <div class="d-flex gap-2">
                                {button}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """
        if not result["output"]:
            logging.warn("No recruiters found in search_recruiter_approval")
            html = """"  <div class="row no-results text-center py-5" id="noResults" style="display: none;">
                <div class="col-12">
                    <i class="fas fa-search fa-3x mb-3 text-muted"></i>
                    <h4>No recruiters found</h4>
                    <p class="text-muted">Try adjusting your search or filter criteria</p>
                </div>
            </div>"""
        return jsonify({"success": True, "data": result["output"], "html": html}), 200
    else:
        logging.error(f"Failed to retrieve recruiters: {result}")
        return jsonify({"success": False, "error": result}), 500



@recruiter_approval.route("/admin/update_recruiter_status", methods=["POST"])
@verify_user
def update_recruiter_status():
    """
    Update the verification status of a recruiter.

    Expected form data or JSON:
        employer_id (int) - Required
        status (str) - Required: 'approved', 'rejected', or 'pending'
        admin_notes (str) - Optional

    Returns:
        JSON response with success or error message.
    """
    data = request.get_json() or request.form

    employer_id = data.get("employer_id")
    new_status = data.get("status")
    admin_notes = data.get("admin_notes", "").strip()

    # Input validation
    if not employer_id:
        logging.warning("Missing employer_id in the request data")
        return jsonify({"success": False, "error": "Missing employer_id"}), 400

    if new_status not in ["approved", "rejected", "pending"]:
        logging.warning(f"Invalid status value: {new_status}")
        return jsonify({"success": False, "error": "Invalid status value"}), 400

    try:
        db_connection = get_db()

        # Build dynamic part of query
        update_fields = {
            "status": new_status
        }

        # Set approved_at only if status is approved
        if new_status == "approved":
            update_fields["approved_at"] = datetime.utcnow()
        else:
            update_fields["approved_at"] = None  # Clear it if not approved

        if admin_notes:
            update_fields["admin_notes"] = admin_notes

        # Generate SQL SET clause dynamically
        set_clause = ", ".join([f"{key} = :{key}" for key in update_fields])
        query = f"""
            UPDATE employer_verification
            SET {set_clause}
            WHERE employer_id = :employer_id
        """

        logging.info(f"Executing update query for employer_id {employer_id} with status '{new_status}'")

        result = db_connection.execute_query(
            text(query),
            {
                "employer_id": employer_id,
                **update_fields
            }
        )

        if result["success"]:
            logging.info(f"Successfully updated employer ID {employer_id} status to '{new_status}'")
            return jsonify({
                "success": True,
                "message": f"Employer ID {employer_id} status updated to '{new_status}'",
                "data": {
                    "employer_id": employer_id,
                    "status": new_status,
                    "admin_notes": admin_notes
                }
            }), 200
        else:
            logging.error(f"Failed to update database for employer ID {employer_id}: {result}")
            return jsonify({"success": False, "error": "Failed to update database", "details": result}), 500

    except Exception as e:
        logging.error(f"Error updating recruiter status for employer ID {employer_id}: {e}")
        return jsonify({"success": False, "error": str(e)}), 500
