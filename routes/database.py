from flask import Blueprint

# Create a Blueprint
database = Blueprint('database', __name__)

# Define your routes using the Blueprint
@database.route('/database')
def home():
    return 'this is the database'
