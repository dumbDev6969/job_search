from flask import Blueprint

from .jobseeker_job_interest import jobseeker_job_interest
from .jobseeker_profile import jobseeker_profile
from .jobseeker_post_job import jobseeker_post_job
from .jobseeker_qualification import jobseeker_qualification
from .jobseeker_find_job import jobseeker_find_job
# Create a Blueprint for the jobseeker module
jobseeker_bp = Blueprint('jobseeker', __name__)

# Register all jobseeker related blueprints

jobseeker_bp.register_blueprint(jobseeker_job_interest)
jobseeker_bp.register_blueprint(jobseeker_profile)
jobseeker_bp.register_blueprint(jobseeker_post_job)
jobseeker_bp.register_blueprint(jobseeker_qualification)
jobseeker_bp.register_blueprint(jobseeker_find_job)
