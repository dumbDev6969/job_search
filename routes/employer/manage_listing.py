from flask import Blueprint,render_template
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
# Create a Blueprint
manage_listing = Blueprint('manage_listing', __name__)

# Define your routes using the Blueprint
@manage_listing.route('/employer/manage_listing')
@verify_user
@is_email_verified
def manage_listing_():
    return render_template('/pages/recruiter/manage_listing.html')
"""
SELECT 
    a.application_id,
    a.status as application_status,
    a.applied_at,
    a.resume_url,
    a.cover_letter,
    j.title as job_title,
    j.description as job_description,
    j.location as job_location,
    j.salary_range,
    j.employment_type,
    CONCAT(js.first_name, ' ', js.last_name) as applicant_name,
    js.email as applicant_email,
    js.phone as applicant_phone,
    js.province as applicant_province
FROM applications a
JOIN jobs j ON a.job_id = j.job_id
JOIN job_seekers js ON a.seeker_id = js.seeker_id
ORDER BY a.applied_at DESC;"""