from flask import Blueprint, render_template,jsonify


# Create a Blueprint for error handlers
db_not_active = Blueprint('db_not_active', __name__)
# Initialize the Limiter

# Register the 404 error handler
@db_not_active.app_errorhandler(404)
def db_not_active_(error):
    return render_template('pages/db_not_active.html'), 404

