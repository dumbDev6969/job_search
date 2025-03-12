from flask import Blueprint

# Create a Blueprint
main = Blueprint('main', __name__)

# Define your routes using the Blueprint
@main.route('/')
def home():
    return 'Home Page'

@main.route('/about')
def about():
    return 'About Page'