from flask import Flask
from routes.routes import main
from routes.database import database
from routes.admin import admin
from routes.chat import chat
from routes.employer import employer
from routes.geo import geo
from routes.interest import interest
from routes.jobs import jobs
from routes.jobseeker import jobseeker
from routes.login import login
from routes.signup import signup
from swagger import swagger_ui_blueprint, SWAGGER_URL

app = Flask(__name__)

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
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)

if __name__ == '__main__':
    app.run(debug=True)