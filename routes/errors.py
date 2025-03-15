from flask import Blueprint, render_template

# Create a Blueprint for error handlers
errors = Blueprint('errors', __name__)

# Register the 404 error handler
@errors.app_errorhandler(404)
def not_found_error(error):
    return render_template('pages/404.html'), 404