from flask import Flask
from datetime import datetime,timedelta
from   job_search.routes.routes import main
from   job_search.routes.database import database
from   job_search.routes.admin import admin
from   job_search.routes.chat import chat
from   job_search.routes.employer import employer
from   job_search.routes.geo import geo
from   job_search.routes.interest import interest
from   job_search.routes.jobs import jobs
from   job_search.routes.jobseeker import jobseeker
from   job_search.routes.login import login
from   job_search.routes.signup import signup
from   job_search.routes.otp import otp
from   job_search.routes.static_files import static_files
from   job_search.routes.jobseeker import jobseeker
from   job_search.routes.logout import logout
from   job_search.routes.errors import errors
from   job_search.routes.dashboard import dashboard


from swagger import swagger_ui_blueprint, SWAGGER_URL



app = Flask(__name__)

# Configure session
app.secret_key = 'your-secret-key-here'  # Replace with a secure secret key in production
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)

# Register the Blueprints
app.register_blueprint(main)
app.register_blueprint(database)
app.register_blueprint(admin)
app.register_blueprint(chat)
app.register_blueprint(employer)
app.register_blueprint(geo)
app.register_blueprint(interest)
app.register_blueprint(jobs)
app.register_blueprint(jobseeker)
app.register_blueprint(login)
app.register_blueprint(signup)
app.register_blueprint(otp)
app.register_blueprint(static_files)
app.register_blueprint(logout)
app.register_blueprint(errors)
app.register_blueprint(dashboard)
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(debug=True)