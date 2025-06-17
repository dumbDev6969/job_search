from flask import Blueprint, render_template, request, redirect, flash
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
from flask import session, redirect
from utils.database import get_db
from sqlalchemy import text
import os
from utils.check_if_exists import check_column_exists

# Create a Blueprint
requirements = Blueprint("requirements", __name__)


# Define your routes using the Blueprint\
@requirements.route("/signup/employer/requirements")
@requirements.route("/signup/requirements")
def requirements_():
    if session.get("user_id"):
        if not session.get("id_step_1_done") and not session.get("user_id"):
            logger.info("User is not logged in, redirecting to signup page.")
            return redirect("/signup/employer")
    else:
        if not session.get("id_step_1_done"):
            logger.info("User has not completed step 1, redirecting to signup page.")
            return redirect("/signup/employer")
    logger.info("Rendering requirements page.")
    return render_template("/pages/recruiter/requirement.html")




@requirements.route("/submit_requirements", methods=["POST"])
def submit_requirements():
    """Handles the submission of recruiter requirements form."""
  

    try:
        db = get_db()
        logger.info("Submitting recruiter requirements form.")

        # Retrieve form data
        business_permit = request.files.get("business_permit")
        tax_id = request.form.get("tax_id")
        supporting_docs = request.files.getlist("supporting_docs[]")
        linkedin = request.form.get("linkedin")
        facebook = request.form.get("facebook")

        # Validate data (basic validation - you might want to add more)
        if not tax_id:
            logger.warning("Tax ID is required.")
            return redirect("/signup/requirements")  # Redirect back to the form

        # Get the employer_id from the session (assuming user is logged in)
        # employer_id = session.get("user_id")  # Or however you store the user ID

        if session['id_step_1_done'] and not session['uuid']:
            logger.warning("User not logged in.")
            return redirect("/login")  # Redirect to login
        is_uuid_valid = check_column_exists("employers", "register_id", session['uuid'])
        logger.info("Given UUID is: %s", session['uuid'])
        logger.info("UUID is valid: %s", is_uuid_valid)
        if is_uuid_valid:
            employer_id_query = text(f"SELECT employer_id FROM employers WHERE register_id = '{session['uuid']}'")
            result = db.execute_query(employer_id_query)
            if result["success"]:
                employer_id = result["output"][0]["employer_id"]
                logger.info("Employer ID was found: %s", employer_id)
        if not employer_id:
            logger.warning("Employer ID not found.")
            return redirect("/signup/requirements")

        # Handle file uploads and get URLs
        business_permit_url = None
        if business_permit:
            business_permit_url = save_file(business_permit, "business_permits")
        supporting_docs_urls = []
        if supporting_docs:
            for doc in supporting_docs:
                url = save_file(doc, "supporting_docs")
                if url:
                    supporting_docs_urls.append(url)
        supporting_docs_urls_str = ",".join(supporting_docs_urls) if supporting_docs_urls else None

        # Prepare data for database insertion
        params = {
            "employer_id": employer_id,
            "business_permit_url": business_permit_url,
            "tax_id_number": tax_id,
            "supporting_docs_urls": supporting_docs_urls_str,
            "linkedin_profile": linkedin,
            "facebook_profile": facebook,
        }

        # Build the SQL query
        query = text(
            """
            INSERT INTO employer_verification (employer_id, business_permit_url, tax_id_number, supporting_docs_urls, linkedin_profile, facebook_profile)
            VALUES (:employer_id, :business_permit_url, :tax_id_number, :supporting_docs_urls, :linkedin_profile, :facebook_profile)
            """
        )

        # Execute the query
        result = db.execute_query(query, params)

        if result["success"]:
            logger.info("Data was inserted.")
            return redirect("/login")  # Redirect to a success page
        else:
            logger.warning("Data was not inserted.")
            logger.warning(result)
            return redirect("/signup/requirements")  # Redirect back to the form

    except Exception as e:
        logger.exception("Error submitting requirements: %s", str(e))
        return redirect("/signup/requirements")  # Redirect back to the form


def save_file(file, upload_folder):
    """Saves a file to the server and returns its URL."""
    if not file:
        logger.info("No file provided for upload.")
        return None

    try:
        # Ensure the upload directory exists
        upload_path = os.path.join("files", upload_folder)
        os.makedirs(upload_path, exist_ok=True)

        # Generate a unique filename
        filename = file.filename
        file_path = os.path.join(upload_path, filename)

        # Save the file
        file.save(file_path)
        logger.info("File saved successfully: %s", file_path)

        # Return the file path (or URL, depending on your setup)
        return "/" + file_path  # Assuming files are served from the root

    except Exception as e:
        logger.error("Error saving file: %s", str(e))
        return None
