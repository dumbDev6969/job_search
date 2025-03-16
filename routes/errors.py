from flask import Blueprint, render_template,jsonify


# Create a Blueprint for error handlers
errors = Blueprint('errors', __name__)
# Initialize the Limiter

# Register the 404 error handler
@errors.app_errorhandler(404)
def not_found_error(error):
    return render_template('pages/404.html'), 404


@errors.app_errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        "error": "Too Many Requests",
        "message": "You have exceeded the allowed number of requests. Please try again later."
    }), 429