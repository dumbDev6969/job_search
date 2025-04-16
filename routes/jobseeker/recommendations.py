from flask import Blueprint,render_template
from middlewares.verify_user import verify_user
from middlewares.is_email_verified import is_email_verified
from middlewares.user_access import jobseeker as jobseeker,admin,emplyer
from middlewares.is_setup_done import is_interests_done,is_qualification_done

# Create a Blueprint
recomendations= Blueprint('recomendations', __name__)

# Define your routes using the Blueprint
@recomendations.route('/jobseeker/recomendations')
@verify_user
@is_email_verified
@is_interests_done
@is_qualification_done
def recomendations_():
    return render_template('/pages/job_seeker/recommendation.html')

