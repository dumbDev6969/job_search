from flask import redirect, session, request,render_template
from functools import wraps


def is_user_logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if 'user_id' in session:
            user_type = session['user_type']
            if user_type == 'seeker':
                return redirect('/jobseeker/dashboard')
            elif user_type == 'employer':
                return redirect('/employer/dashboard')
            elif user_type == 'admin':
                return redirect('/admin/dashboard')

        return f(*args, **kwargs)
    return decorated_function
        