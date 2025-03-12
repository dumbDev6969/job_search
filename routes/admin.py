from flask import Blueprint

# Create a Blueprint
admin = Blueprint('admin', __name__)

# Define your routes using the Blueprint
@admin.route('/admin')
def home():
    return 'Admin Page'