from flask import Blueprint, render_template

from utils.database import get_db
from utils.check_if_exists import check_column_exists
from middlewares.is_email_verified import is_email_verified
from middlewares.verify_user import verify_user
from sqlalchemy import text

employer_profile = Blueprint("employer_profile", __name__)


@employer_profile.route("/employer/<int:employer_id>")
def employer_details(employer_id):
    """
    Render the employer's details page with dynamic data.
    """
    if not check_column_exists("employers", "employer_id", employer_id):
        return render_template("/pages/user_not_found.html")

    db = get_db()

    sql = text("""
        SELECT
            e.employer_id,
            e.company_name,
            e.email,
            e.website,
            e.logo_url,
            e.industry,
            e.company_size,
            COUNT(j.job_id) as jobs_posted
        FROM employers e
        LEFT JOIN jobs j ON e.employer_id = j.employer_id
        WHERE e.employer_id = :employer_id
        GROUP BY e.employer_id
    """)

    result = db.execute_query(sql, {"employer_id": employer_id})
    if not result["success"] or not result["output"]:
        return render_template(
            "/pages/recruiter/recruiter_details.html", error="Employer not found."
        )

    return render_template(
        "/pages/recruiter/recruiter_details.html", employer=result["output"][0]
    )
