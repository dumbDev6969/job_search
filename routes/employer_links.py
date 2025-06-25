from flask import Blueprint, request, jsonify
from utils.get_file_paths import get_employer_links

employer_links = Blueprint('employer_links', __name__)

@employer_links.route('/api/employer/<int:id>/links')
def get_links(id):
    try:
        links = get_employer_links(id)
        return jsonify(links)
    except Exception as e:
        return jsonify({'error': str(e)}), 500