from flask import Blueprint, render_template
import sqlite3
from middlewares.verify_user import verify_user
# Create a Blueprint
database = Blueprint('database', __name__)

# Define your routes using the Blueprint
@database.route('/database')
def home():
    return 'this is the database'

@database.route('/admin/database/history')
# @verify_user
def history():
    # Connect to the SQLite database
    conn = sqlite3.connect('utils/query_logs.db')
    conn.row_factory = sqlite3.Row  # This enables column access by name
    cursor = conn.cursor()
    
    # Fetch all query logs
    cursor.execute('SELECT * FROM query_logs ORDER BY execution_time DESC')
    query_logs = cursor.fetchall()
    
    # Close the connection
    conn.close()
    
    # Render the template with the query logs
    return render_template('pages/database_history.html', query_logs=query_logs)
