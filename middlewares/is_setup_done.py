from flask import redirect, session, request,render_template
from functools import wraps
from utils.check_if_exists import check_if_exists

def is_qualification_done(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if 'user_id' in session:
            user_type = session['user_type']
            if user_type == 'seeker':
                is_done = check_if_exists('qualification', 'seeker_id', session['user_id'])
                if not is_done:
                    return redirect('/qualification')
        return f(*args, **kwargs)
    return decorated_function
        

def is_interests_done(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if 'user_id' in session:
            user_type = session['user_type']
            if user_type =='seeker':
                is_done = check_if_exists('interest','seeker_id', session['user_id'])
                if not is_done:
                    return redirect('/interests')