# from flask import Blueprint,Flask,render_template,redirect

# # Import route blueprints
# from routes.database import database
# from routes.geo import geo
# from routes.login import login
# from routes.signup import signup
# from routes.otp import otp
# from routes.static_files import static_files
# from routes.logout import logout
# from routes.errors import errors
# from routes.dashboard import dashboard
# from routes.forgot_password import forgot_password
# from routes.routes import main
# from swagger import swagger_ui_blueprint, SWAGGER_URL
# from routes.database_not_active import db_not_active
# from utils.database import test_mysql
# from routes.jobseeker import jobseeker_bp
# from routes.employer import employer_bp
# from routes.admin import admin_bp
# from routes.messages import messages_bp
# from routes.messages import *

# routes_bp = Blueprint('routes', __name__)


# is_first=True
# is_mysql_running = False
# # Register the Blueprints
# def test_connection():
#     print("testing connection")
#     global is_mysql_running
#     is_mysql_running = test_mysql()
#     print("is_mysql_running",is_mysql_running)
#     if is_mysql_running:
#         # Core routes
#         routes_bp.register_blueprint(main)
#         routes_bp.register_blueprint(database)
#         routes_bp.register_blueprint(geo)
#         routes_bp.register_blueprint(login)
#         routes_bp.register_blueprint(signup)
#         routes_bp.register_blueprint(otp)
#         routes_bp.register_blueprint(static_files)
#         routes_bp.register_blueprint(logout)
#         routes_bp.register_blueprint(errors)
#         routes_bp.register_blueprint(dashboard)
#         routes_bp.register_blueprint(jobseeker_bp)
#         routes_bp.register_blueprint(forgot_password)
#         routes_bp.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
#         # Employer/Admin/Messaging
#         routes_bp.register_blueprint(employer_bp)
#         routes_bp.register_blueprint(admin_bp)
#         routes_bp.register_blueprint(messages_bp)
#     else:
#         global is_first
#         if is_first:
#            print("registering error handler")
#            routes_bp.register_blueprint(db_not_active)
#            is_first=False


# test_connection()

# @routes_bp.route('/retry')
# def retry():
#     test_connection()
#     if not is_mysql_running:
#         return render_template('pages/db_not_active.html'), 404
#     return redirect('/')

from flask import Blueprint, render_template, redirect, request, url_for,session
from utils.database import test_mysql

from middlewares.is_employer_verified import is_employer_verified
from utils.database import get_db
from utils.check_if_exists import check_column_exists
# Import route blueprints
from routes.database import database
from routes.geo import geo
from routes.login import login
from routes.signup import signup
from routes.otp import otp
from routes.static_files import static_files
from routes.logout import logout
from routes.errors import errors
from routes.dashboard import dashboard
from routes.forgot_password import forgot_password
from routes.routes import main
from swagger import swagger_ui_blueprint, SWAGGER_URL
from routes.database_not_active import db_not_active
from routes.jobseeker import jobseeker_bp
from routes.employer import employer_bp
from routes.admin import admin_bp
from routes.messages import *



# Create the routes blueprint
routes_bp = Blueprint('routes', __name__)

# Global flag to track DB status
is_mysql_running = False

# Register all blueprints unconditionally
routes_bp.register_blueprint(main)
routes_bp.register_blueprint(database)
routes_bp.register_blueprint(geo)
routes_bp.register_blueprint(login)
routes_bp.register_blueprint(signup)
routes_bp.register_blueprint(otp)
routes_bp.register_blueprint(static_files)
routes_bp.register_blueprint(logout)
routes_bp.register_blueprint(errors)
routes_bp.register_blueprint(dashboard)
routes_bp.register_blueprint(forgot_password)
routes_bp.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
routes_bp.register_blueprint(jobseeker_bp)
routes_bp.register_blueprint(employer_bp)
routes_bp.register_blueprint(admin_bp)
routes_bp.register_blueprint(messages_bp)
routes_bp.register_blueprint(db_not_active)  # Always register this for fallback

# Check database status at startup
def check_mysql_connection():
    global is_mysql_running
    is_mysql_running = test_mysql()
  
check_mysql_connection()

# Before request hook to control access based on DB status
@routes_bp.before_request
def before_request():
    logging.warning("="*100)
    logging.error(session)
    global is_mysql_running
    session['is_database_running'] = True
    if not is_mysql_running:
        session['is_database_running'] = False
        if request.endpoint != 'routes.retry' and not request.path.startswith('/static'):
            return redirect(url_for('routes.retry'))
    if 'user_id' in session and request.path.startswith('/employer'):
            logging.info(f"Checking if user with id {session['user_id']} is verified")
            if  check_column_exists('employers', 'employer_id ', session['user_id']):
                logging.info(f"Checking if employer with id {session['user_id']} is verified")
                if not check_column_exists('employer_verification', 'employer_id', session['user_id']):
                    logging.info(f"Employer with id {session['user_id']} is not verified")
                    return redirect('/signup/employer/requirements')
                db= get_db()
                sql = text("SELECT * FROM employer_verification WHERE employer_id  = :employer_id")
                result = db.execute_query(sql, {'employer_id': session['user_id'], 'status': 'approved'})
                if result:
                    logging.info(f"Employer with id {session['user_id']} is verified")
                else:
                    logging.info(f"Employer with id {session['user_id']} is not verified")
                # return result
                if result['output']:
                    status = result['output'][0]['status']
                    # return result
                    logging.info(f"Employer with id {session['user_id']} has status {status}")
                    if status == 'approved':
                        logging.info(f"Employer with id {session['user_id']} is verified")
                        session['is_employer_verified'] = True
                        pass
                    elif status == 'pending':
                        logging.info(f"Employer with id {session['user_id']} is not verified")
                        session['is_employer_verified'] = False
                        return render_template('/pages/account_pending.html')
                    elif status == 'rejected':
                        logging.info(f"Employer with id {session['user_id']} is not verified")
                        session['is_employer_verified'] = False
                        return render_template('/pages/account_rejected.html')



   
# Retry route
@routes_bp.route('/retry')
def retry():
    global is_mysql_running
    is_mysql_running = test_mysql()
    if is_mysql_running:
        return redirect('/')
    return render_template('pages/db_not_active.html'), 404