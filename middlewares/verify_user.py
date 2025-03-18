from flask import redirect, session, request, render_template
from functools import wraps

def verify_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            print("user is not logged in")
            return redirect('/login')
        
        user_type = session['user_type']
        current_path = request.path
        
        # Define allowed paths for each user type
        allowed_paths = {
            'seeker': ['/jobseeker','/dashboard'],
            'employer': ['/employer', '/pages/recruiter','/dashboard',],
            'admin': ['/admin','/dashboard']
        }
        
        # Check if user is accessing allowed paths
        user_allowed_paths = allowed_paths.get(user_type, [])
        if not any(current_path.startswith(path) for path in user_allowed_paths):
            print(f"User {user_type} attempting unauthorized access")
            return render_template("pages/unauthorized.html")
        
        return f(*args, **kwargs)
    return decorated_function
