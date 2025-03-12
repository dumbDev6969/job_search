from flask import Blueprint

# Create a Blueprint
jobs = Blueprint('jobs', __name__)

# Define your routes using the Blueprint
@jobs.route('/jobs')
def home():
    return 'Jobs Page'