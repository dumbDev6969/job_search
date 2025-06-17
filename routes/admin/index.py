from flask import Blueprint,render_template
from middlewares.verify_user import verify_user

# Create a Blueprint
index = Blueprint('index', __name__)

# Define your routes using the Blueprint
@index.route('/admin/')
@index.route('/admin/')
@index.route('/admin/index')
@index.route('/admin/dashboard.html')
@index.route('/admin/dashboard')
@index.route('/admin/dashboard/')
@verify_user
def index_():
    return render_template('/pages/admin/index.html')