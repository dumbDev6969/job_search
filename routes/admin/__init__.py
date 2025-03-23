from .index import index
from .stats import stats
from flask import Blueprint


admin_bp = Blueprint('admin_bp', __name__)

admin_bp.register_blueprint(index)
admin_bp.register_blueprint(stats)