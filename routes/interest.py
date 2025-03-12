from flask import Blueprint

# Create a Blueprint
interest = Blueprint('interest', __name__)

# Define your routes using the Blueprint
@interest.route('/interest')
def home():
    return 'Interest Page'