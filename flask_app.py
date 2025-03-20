from flask import Flask,request
from datetime import datetime,timedelta
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from swagger import swagger_ui_blueprint, SWAGGER_URL
import os
from utils.database import test_mysql

app = Flask(__name__)


# Import routes
from routes.routes import main
from routes.database import database
from routes.admin import admin
from routes.chat import chat
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
# from routes.jobseeker_jobs import jobseeker_job
# from routes.jobseeker_profile import jobseeker_profile
# from routes.jobseeker_qualification import jobseeker_qualification
# from routes.jobseeker_dashboard import jobseeker
from routes.jobseeker import jobseeker_bp
# Configure session
app.secret_key = os.environ.get('secret')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)



limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)
limiter.init_app(app)

# Register the Blueprints
app.register_blueprint(main)
app.register_blueprint(database)
app.register_blueprint(admin)
app.register_blueprint(chat)
app.register_blueprint(employer)
app.register_blueprint(geo)
app.register_blueprint(interest)
app.register_blueprint(login)
app.register_blueprint(signup)
app.register_blueprint(otp)
app.register_blueprint(static_files)
app.register_blueprint(logout)
app.register_blueprint(errors)
app.register_blueprint(dashboard)
app.register_blueprint(jobseeker_bp)
app.register_blueprint(forgot_password)
# app.register_blueprint(jobseeker)
# app.register_blueprint(jobseeker_job)
# app.register_blueprint(jobseeker_profile)
# app.register_blueprint(jobseeker_qualification)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
# Apply rate limiting to specific routes
limiter.limit("5/minute")(login)
limiter.limit("3/minute")(otp)
limiter.limit("5/minute")(signup)

if __name__ == '__main__':
    test = test_mysql()
    if test:
        print("Database connected")
        app.run(debug=True)
    else:
        print("Database not connected")
        from routes.databse_notactive import db_not_active
        app1 = Flask(__name__)
        app1.register_blueprint(db_not_active)
        app1.run(debug=True)
