from flask import Blueprint, render_template, current_app
from .messages import messages

# Create a Blueprint
main = Blueprint('main', __name__)

# Define your routes using the Blueprint
@main.route('/')
def home():
    return render_template("/pages/index.html")

@main.route('/about')
def about():
    return 'About Page'

# Register the messages blueprint
from flask import request, jsonify
from utils.database import get_db

def init_app(app):
    app.register_blueprint(messages)

    @app.route('/api/submit_verification', methods=['POST'])
    def submit_verification():
        try:
            data = request.form
            # Validate data
            employer_id = 1 # TODO: Get employer_id from session or other authentication method
            business_permit_url = data.get('business_permit')
            tax_id_number = data.get('tax_id')
            supporting_docs_urls = ','.join(data.getlist('supporting_docs[]'))
            linkedin_profile = data.get('linkedin')
            facebook_profile = data.get('facebook')

            if not all([business_permit_url, tax_id_number]):
                return jsonify({'success': False, 'message': 'Missing required fields'}), 400

            db = get_db()
            query = text("""
                INSERT INTO employer_verification (employer_id, business_permit_url, tax_id_number, supporting_docs_urls, linkedin_profile, facebook_profile)
                VALUES (:employer_id, :business_permit_url, :tax_id_number, :supporting_docs_urls, :linkedin_profile, :facebook_profile)
            """)
            params = {
                'employer_id': employer_id,
                'business_permit_url': business_permit_url,
                'tax_id_number': tax_id_number,
                'supporting_docs_urls': supporting_docs_urls,
                'linkedin_profile': linkedin_profile,
                'facebook_profile': facebook_profile
            }
            result = db.execute_query(query, params)

            if result['success']:
                return jsonify({'success': True, 'message': 'Verification data submitted successfully'})
            else:
                return jsonify({'success': False, 'message': result['message']}), 500

        except Exception as e:
            return jsonify({'success': False, 'message': str(e)}), 500
