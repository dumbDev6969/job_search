from flask import Blueprint, request, jsonify
from utils.get_file_paths import get_employer_logo

employer_logo = Blueprint('employer_logo', __name__)

@employer_logo.route('/api/employer/<int:id>/logo')
def get_logo(id):
    try:
        logo_url = get_employer_logo(id)
        if logo_url:
            return jsonify({'logo_url': logo_url})
        else:
            return jsonify({'error': 'Logo not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500