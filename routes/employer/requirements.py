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
    if  session.get('user_id'):
        if not session.get('id_step_1_done') and not session.get('user_id'):
            return redirect("/signup/employer")
    else:
        if not session.get('id_step_1_done'):
            return redirect("/signup/employer")
    return render_template("/pages/recruiter/requirement.html")


@requirements.route("/submit_requirements", methods=["POST"])
def submit_requirements():
    """Handles the submission of recruiter requirements form."""
    try:
        db = get_db()
        print("accpting from")
        # Retrieve form data
        business_permit = request.files.get("business_permit")
        tax_id = request.form.get("tax_id")
        supporting_docs = request.files.getlist("supporting_docs[]")
        linkedin = request.form.get("linkedin")
        facebook = request.form.get("facebook")

        # Validate data (basic validation - you might want to add more)
        if not tax_id:
            print("Tax ID is required.", "error")
            return redirect("/signup/requirements")  # Redirect back to the form

        # Get the employer_id from the session (assuming user is logged in)
        # employer_id = session.get("user_id")  # Or however you store the user ID

        if session['id_step_1_done'] and not session['uuid']:
            print("User not logged in.", "error")
            return redirect("/login")  # Redirect to login
        is_uuid_valid = check_column_exists("employers", "register_id", session['uuid'])
        print("thr giveen uuid is:", session['uuid'],is_uuid_valid)
        if is_uuid_valid:
            employer_id_query = text(f"SELECT employer_id FROM employers WHERE register_id = '{session['uuid']}'")
            result = db.execute_query(employer_id_query)
            if result["success"]:
                employer_id = result["output"][0]["employer_id"]
                print("the employer id was found")
        if not employer_id:
            print("Employer ID not found.", "error")
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
            print("the data was inserted/n")
            return redirect("/login")  # Redirect to a success page
        else:
            print("the data was not inserted/n")
            print(result)
            return redirect("/signup/requirements")  # Redirect back to the form

    except Exception as e:
        print(f"Error submitting requirements: {str(e)}/n")
        return redirect("/signup/requirements")  # Redirect back to the form


def save_file(file, upload_folder):
    """Saves a file to the server and returns its URL."""
    if not file:
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

        # Return the file path (or URL, depending on your setup)
        return "/" + file_path  # Assuming files are served from the root

    except Exception as e:
        print(f"Error saving file: {str(e)}")
        return None
