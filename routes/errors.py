from flask import Blueprint, render_template,jsonify,session


# Create a Blueprint for error handlers
errors = Blueprint('errors', __name__)
# Initialize the Limiter

# Register the 404 error handler
@errors.app_errorhandler(404)
def not_found_error(error):
    if session['is_database_running']:
        return render_template('pages/db_not_active.html'), 404
    else:
        return render_template('pages/404.html'), 404


@errors.app_errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        "error": "Too Many Requests",
        "message": "You have exceeded the allowed number of requests. Please try again later."
    }), 429