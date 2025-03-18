from flask import Blueprint, send_from_directory, abort, current_app, request
import os
import mimetypes
import logging
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a Blueprint
static_files = Blueprint('static_files', __name__)


# Allowed file types
ALLOWED_EXTENSIONS = {
    'css', 'js', 'png', 'jpg', 'jpeg', 'gif', 'svg',
    'woff', 'woff2', 'ttf', 'eot', 'ico', 'json'
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def add_cache_headers(response):
    # Cache static files for 1 week
    response.cache_control.public = True
    response.cache_control.max_age = 604800  # 1 week in seconds
    response.expires = datetime.now() + timedelta(days=7)
    return response

@static_files.route('/static/<path:filename>')
def serve_static(filename):
    """
    Serve static files from the static directory with caching and security measures.
    
    Args:
        filename (str): The path to the file within the static directory
        
    Returns:
        The requested file if it exists, appropriate error response otherwise
    """
    if not allowed_file(filename):
        logger.warning(f"Attempted access to unauthorized file type: {filename}")
        return abort(403)

    try:
        static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
        response = send_from_directory(static_dir, filename)
        logger.info(f"Serving static file: {filename}")
        return add_cache_headers(response)
    except Exception as e:
        logger.error(f"Error serving static file {filename}: {str(e)}")
        return abort(404)

@static_files.route('/auth/<path:filename>')
def serve_auth_static(filename):
    """
    Serve static files from the auth directory with caching and security measures.
    
    Args:
        filename (str): The path to the file within the auth directory
        
    Returns:
        The requested file if it exists, appropriate error response otherwise
    """
    if not allowed_file(filename):
        logger.warning(f"Attempted access to unauthorized file type in auth: {filename}")
        return abort(403)

    try:
        static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'auth')
        response = send_from_directory(static_dir, filename)
        logger.info(f"Serving auth static file: {filename}")
        return add_cache_headers(response)
    except Exception as e:
        logger.error(f"Error serving auth static file {filename}: {str(e)}")
        return abort(404)

@static_files.route('/assets/<path:filename>')
def serve_assets(filename):
    """
    Serve static files from the assets directory with caching and security measures.
    
    Args:
        filename (str): The path to the file within the assets directory
        
    Returns:
        The requested file if it exists, appropriate error response otherwise
    """
    if not allowed_file(filename):
        logger.warning(f"Attempted access to unauthorized file type in assets: {filename}")
        return abort(403)

    try:
        static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'assets')
        response = send_from_directory(static_dir, filename)
        logger.info(f"Serving asset file: {filename}")
        return add_cache_headers(response)
    except Exception as e:
        logger.error(f"Error serving asset file {filename}: {str(e)}")
        return abort(404)

@static_files.route('/javascript/<path:filename>')
def serve_javascript(filename):
    """
    Serve JavaScript files from the javascript directory with caching and security measures.
    
    Args:
        filename (str): The path to the file within the javascript directory
        
    Returns:
        The requested file if it exists, appropriate error response otherwise
    """
    if not allowed_file(filename):
        logger.warning(f"Attempted access to unauthorized file type in javascript: {filename}")
        return abort(403)

    try:
        static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'javascript')
        response = send_from_directory(static_dir, filename)
        logger.info(f"Serving javascript file: {filename}")
        return add_cache_headers(response)
    except Exception as e:
        logger.error(f"Error serving javascript file {filename}: {str(e)}")
        return abort(404)