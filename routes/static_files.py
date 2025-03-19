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


def is_safe_path(path):
    """Check if the path is safe to serve."""
    # Normalize path and check for directory traversal attempts
    normalized = os.path.normpath(path)
    return not normalized.startswith('..')

def add_cache_headers(response):
    # Cache static files for 1 week
    response.cache_control.public = True
    response.cache_control.max_age = 604800  # 1 week in seconds
    response.expires = datetime.now() + timedelta(days=7)
    return response

@static_files.route('/<path:filepath>')
def serve_static_files(filepath):
    """
    Serve all static files from any subdirectory under /static with security measures.
    
    Args:
        filepath (str): The path to the file within the static directory
        
    Returns:
        The requested file if it exists and is safe, appropriate error response otherwise
    """
    if not is_safe_path(filepath):
        logger.warning(f"Attempted directory traversal: {filepath}")
        return abort(403)

    try:
        # Get the base static directory
        static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
        
        # Ensure the requested file is within the static directory
        requested_path = os.path.join(static_dir, filepath)
        if not os.path.commonpath([requested_path, static_dir]) == static_dir:
            logger.warning(f"Attempted access outside static directory: {filepath}")
            return abort(403)

        # Get the directory and filename
        dir_path = os.path.dirname(requested_path)
        filename = os.path.basename(requested_path)

        response = send_from_directory(dir_path, filename)
        logger.info(f"Serving static file: {filepath}")
        return add_cache_headers(response)
    except Exception as e:
        logger.error(f"Error serving static file {filepath}: {str(e)}")
        return abort(404)