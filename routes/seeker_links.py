from flask import Blueprint, request, jsonify
from utils.get_file_paths import get_seeker_links

seeker_links = Blueprint('seeker_links', __name__)

@seeker_links.route('/api/seeker/<int:id>/links')
def get_links(id):
    try:
        links = get_seeker_links(id)
        return jsonify(links)
    except Exception as e:
        return jsonify({'error': str(e)}), 500