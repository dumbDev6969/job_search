from flask import Blueprint,render_template,session,redirect

# Create a Blueprint
jobseeker = Blueprint('jobseeker', __name__)

# Define your routes using the Blueprint
@jobseeker.route('/job_seeker/dashboard')
def job_seeker_dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    if session['user_type'] != 'seeker':
        return redirect('/login')
    return render_template("/pages/job_seeker/dashboard.html")