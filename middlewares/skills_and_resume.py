from flask import redirect, session
from functools import wraps
from utils.check_if_exists import check_column_exists

def is_skills_and_resume_done(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' in session:
            if not check_column_exists('seeker_profiles', 'user_id ', session['user_id']):
                return redirect('/jobseeker/skills-and-resume')
               
        return f(*args, **kwargs)
    return decorated_function