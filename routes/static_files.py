from flask import Blueprint, send_from_directory, abort
import os

# Create a Blueprint
static_files = Blueprint('static_files', __name__)

@static_files.route('/static/<path:filename>')
def serve_static(filename):
    """
    Serve static files from the static directory.
    
    Args:
        filename (str): The path to the file within the static directory
        
    Returns:
        The requested file if it exists, 404 error otherwise
    """
    try:
        # Get the absolute path to the static directory
        static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static')
        return send_from_directory(static_dir, filename)
    except Exception as e:
        abort(404)

@static_files.route('/auth/<path:filename>')
def serve_auth_static(filename):
    """
    Serve static files from the auth directory within static.
    
    Args:
        filename (str): The path to the file within the auth directory
        
    Returns:
        The requested file if it exists, 404 error otherwise
    """
    try:
        # Get the absolute path to the auth directory within static
        static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'auth')
        return send_from_directory(static_dir, filename)
    except Exception as e:
        abort(404)

@static_files.route('/assets/<path:filename>')
def serve_assets(filename):
    """
    Serve static files from the assets directory within static.
    
    Args:
        filename (str): The path to the file within the assets directory
        
    Returns:
        The requested file if it exists, 404 error otherwise
    """
    try:
        # Get the absolute path to the assets directory within static
        static_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'static', 'assets')
        return send_from_directory(static_dir, filename)
    except Exception as e:
        abort(404)