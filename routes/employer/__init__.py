from .applicants import applicants
from .company_details import company_details
from .dashboard import dashboard
from .find_talent import find_talent
from .jobs import jobs
from .manage_listing import manage_listing
from .profile import profile

from flask import Blueprint


employer_bp = Blueprint('employer_bp', __name__)

employer_bp.register_blueprint(applicants)
employer_bp.register_blueprint(company_details)
employer_bp.register_blueprint(dashboard)
employer_bp.register_blueprint(find_talent)
employer_bp.register_blueprint(jobs)
employer_bp.register_blueprint(manage_listing)
employer_bp.register_blueprint(profile)