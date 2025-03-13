from flask import Blueprint, render_template

# Create a Blueprint
main = Blueprint('main', __name__)

# Define your routes using the Blueprint
@main.route('/')
def home():
    return render_template("/pages/index.html")

@main.route('/about')
def about():
    return 'About Page'