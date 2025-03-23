from flask import Blueprint,render_template
from middlewares.verify_user import verify_user
from utils.database import get_db
from sqlalchemy import text
# Create a Blueprint
stats = Blueprint('stats', __name__)

# Define your routes using the Blueprint
@stats.route('/api/stats')
def stats_():
    db = get_db()
    employers = db.execute_query(text("SELECT COUNT(*) FROM employers"))
    jobseekers = db.execute_query(text("SELECT COUNT(*) FROM job_seekers"))
    jobs = db.execute_query(text("SELECT COUNT(*) FROM jobs"))
    applications = db.execute_query(text("SELECT COUNT(*) FROM applications"))
    return {
        "employers": employers['output'][0]['COUNT(*)'] if employers['success'] else 0,
        "jobseekers": jobseekers['output'][0]['COUNT(*)'] if jobseekers['success'] else 0,
        "jobs": jobs['output'][0]['COUNT(*)'] if jobs['success'] else 0,
        "applications": applications['output'][0]['COUNT(*)'] if applications['success'] else 0
    }
