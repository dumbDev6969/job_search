from flask import Blueprint, render_template,jsonify,session


# Create a Blueprint for error handlers
db_not_active = Blueprint('db_not_active', __name__)
# Initialize the Limiter

# Register the 404 error handler
@db_not_active.app_errorhandler(404)
def db_not_active_(error):
    if not session['is_database_running']:
        return render_template('pages/db_not_active.html'), 404
    else:
        return render_template('pages/404.html'), 404



