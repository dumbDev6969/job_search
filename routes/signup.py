from flask import Blueprint

# Create a Blueprint
signup = Blueprint('signup', __name__)

# Define your routes using the Blueprint
@signup.route('/signup')
def home():
    return 'Signup Page'