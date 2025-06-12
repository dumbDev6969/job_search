from flask import redirect, session, request,render_template
from functools import wraps
from utils.check_if_exists import check_column_exists

def is_requirements_done(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' in session:
            pass
            # return redirect('/employer/requirements')
               
        return f(*args, **kwargs)
    return decorated_function