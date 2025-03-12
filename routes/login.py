from flask import Blueprint

# Create a Blueprint
login = Blueprint('login', __name__)

# Define your routes using the Blueprint
@login.route('/login')
def home():
    return 'Login Page'