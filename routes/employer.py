from flask import Blueprint

# Create a Blueprint
employer = Blueprint('employer', __name__)

# Define your routes using the Blueprint
@employer.route('/employer')
def home():
    return 'Employer Page'