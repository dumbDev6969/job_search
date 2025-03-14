from flask import Blueprint,render_template,session,redirect

# Create a Blueprint
jobseeker = Blueprint('jobseeker', __name__)

# Define your routes using the Blueprint
@jobseeker.route('/job_seeker/dashboard')
def job_seeker_dashboard():
    print(session)
    if 'user_id' in session:
        if session['user_type'] == 'seeker':
            return redirect('/job_seeker/dashboard')
        else:
            return redirect('/login')
    else:
        return redirect('/login')
    return render_template("/pages/job_seeker/dashboard.html")