from flask import Blueprint

# Create a Blueprint
jobseeker = Blueprint('jobseeker', __name__)

# Define your routes using the Blueprint
@jobseeker.route('/jobseeker')
def home():
    return 'Jobseeker Page'