from .applicants import applicants
from .company_details import company_details
from .company_dashboard import company_dashboard
from .dashboard import dashboard
from .edit_job import edit_job
from .find_talent import find_talent
from .job_details import job_details
from .jobs import jobs
from .manage_listing import manage_listing
from .profile import profile
from .schedule_dashboard import schedule_dashboard
from .schedule_interview import schedule_interview
from .employer_profile import employer_profile
from .requirements import requirements

from flask import Blueprint


employer_bp = Blueprint('employer_bp', __name__)

employer_bp.register_blueprint(applicants)
employer_bp.register_blueprint(company_details)
employer_bp.register_blueprint(company_dashboard)
employer_bp.register_blueprint(dashboard)
employer_bp.register_blueprint(edit_job)
employer_bp.register_blueprint(find_talent)
employer_bp.register_blueprint(job_details)
employer_bp.register_blueprint(jobs)
employer_bp.register_blueprint(manage_listing)
employer_bp.register_blueprint(profile)
employer_bp.register_blueprint(schedule_dashboard)
employer_bp.register_blueprint(schedule_interview)
employer_bp.register_blueprint(employer_profile)
employer_bp.register_blueprint(requirements)