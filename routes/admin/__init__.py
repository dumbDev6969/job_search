from .index import index
from .stats import stats
from .job_approval import job_approval
from .recruiter_approval import recruiter_approval
from flask import Blueprint


admin_bp = Blueprint('admin_bp', __name__)

admin_bp.register_blueprint(index)
admin_bp.register_blueprint(stats)
admin_bp.register_blueprint(job_approval)
admin_bp.register_blueprint(recruiter_approval)