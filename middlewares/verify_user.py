from flask import redirect, session, request
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
            'seeker': ['/job_seeker'],
            'employer': ['/employer', '/pages/recruiter'],
            'admin': ['/admin']
        }
        
        # Check if user is accessing allowed paths
        user_allowed_paths = allowed_paths.get(user_type, [])
        if not any(current_path.startswith(path) for path in user_allowed_paths):
            print(f"redirecting {user_type} to their dashboard")
            if user_type == 'seeker':
                return redirect('/job_seeker/dashboard')
            elif user_type == 'employer':
                return redirect('/employer/dashboard')
            elif user_type == 'admin':
                return redirect('/admin/dashboard')
        
        return f(*args, **kwargs)
    return decorated_function
        