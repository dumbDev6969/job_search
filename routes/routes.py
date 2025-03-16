from flask import Blueprint, render_template, stream_template, current_app

# Create a Blueprint
main = Blueprint('main', __name__)

# Define your routes using the Blueprint
@main.route('/')
def home():
    return stream_template("/pages/index.html")

@main.route('/about')
def about():
    return 'About Page'
