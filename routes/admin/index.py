from flask import Blueprint,render_template,request
import requests
import json
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


def get_ip():
    response = requests.get('https://api64.ipify.org?format=json').json()
    return response["ip"]

@index.route('/track')
def track():
    ip_address = get_ip()
    response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    location_data = {
        "ip": ip_address,
        "city": response.get("city"),
        "region": response.get("region"),
        "country": response.get("country_name")
    }
    return location_data