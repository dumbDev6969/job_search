from flask import Blueprint,Flask


from routes.database import database
from routes.admin import admin
from routes.employer import employer
from routes.geo import geo
from routes.interest import interest
from routes.login import login
from routes.signup import signup
from routes.otp import otp
from routes.static_files import static_files
from routes.logout import logout
from routes.errors import errors
from routes.dashboard import dashboard
from routes.forgot_password import forgot_password
from routes.jobseeker import jobseeker_bp
from routes.routes import main
from swagger import swagger_ui_blueprint, SWAGGER_URL
from routes.database_not_active import db_not_active
from utils.database import test_mysql

routes_bp = Blueprint('routes', __name__)



# Register the Blueprints
is_mysql_running = test_mysql()
if is_mysql_running:
    routes_bp.register_blueprint(main)
    routes_bp.register_blueprint(database)
    routes_bp.register_blueprint(admin)
    routes_bp.register_blueprint(employer)
    routes_bp.register_blueprint(geo)
    routes_bp.register_blueprint(interest)
    routes_bp.register_blueprint(login)
    routes_bp.register_blueprint(signup)
    routes_bp.register_blueprint(otp)
    routes_bp.register_blueprint(static_files)
    routes_bp.register_blueprint(logout)
    routes_bp.register_blueprint(errors)
    routes_bp.register_blueprint(dashboard)
    routes_bp.register_blueprint(jobseeker_bp)
    routes_bp.register_blueprint(forgot_password)
    # routes_bp.register_blueprint(jobseeker)
    # routes_bp.register_blueprint(jobseeker_job)
    # routes_bp.register_blueprint(jobseeker_profile)
    # routes_bp.register_blueprint(jobseeker_qualification)
    routes_bp.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
else:
    routes_bp.register_blueprint(db_not_active)



