from flask import Blueprint, render_template, request, jsonify
import sqlite3
from datetime import datetime, timedelta
import logging
from middlewares.verify_user import verify_user

# Create a Blueprint
database = Blueprint('database', __name__)

# Define your routes using the Blueprint
@database.route('/database')
def home():
    return 'this is the database'
@database.route('/admin/database/history')
@verify_user
def history():
    logging.info("Rendering database history page for admin")
    return render_template('pages/admin/database_history.html')



@database.route('/admin/database/history/data')
@verify_user
def history_data():
    # Get query parameters
    start_date = request.args.get('start_date', (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'))
    end_date = request.args.get('end_date', datetime.now().strftime('%Y-%m-%d'))
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    logging.info(f"Fetching database history data for date range {start_date} to {end_date}, page {page}, per_page {per_page}")
    
    # Calculate offset
    offset = (page - 1) * per_page
    
    # Connect to the SQLite database
    conn = sqlite3.connect('utils/query_logs.db')
    conn.row_factory = sqlite3.Row  # This enables column access by name
    cursor = conn.cursor()
    logging.debug("Connected to query_logs.db")
    
    # Get total count for pagination
    cursor.execute(
        'SELECT COUNT(*) FROM query_logs WHERE DATE(execution_time) BETWEEN ? AND ?',

        (start_date, end_date)
    )
    total_count = cursor.fetchone()[0]
    total_pages = (total_count + per_page - 1) // per_page
    
    # Fetch filtered and paginated query logs
    cursor.execute(
        'SELECT * FROM query_logs WHERE DATE(execution_time) BETWEEN ? AND ? '

        'ORDER BY execution_time DESC LIMIT ? OFFSET ?',
        (start_date, end_date, per_page, offset)
    )
    query_logs = [dict(row) for row in cursor.fetchall()]
    logging.info(f"Fetched {len(query_logs)} query logs")
    
    # Close the connection
    conn.close()
    
    return jsonify({
        'logs': query_logs,
        'total_pages': total_pages,
        'current_page': page
    })
