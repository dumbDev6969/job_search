from flask import redirect, session, request,render_template
from functools import wraps


def jobseeker(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not(session.get('user_type') == 'seeker'):
            return render_template("pages/unauthorized.html")
            # return redirect('/login')
    
        return f(*args, **kwargs)
    return decorated_function



def emplyer(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not(session.get('user_type') == 'employer'):
                return render_template("pages/unauthorized.html")
                # return redirect('/login')
    
    
        return f(*args, **kwargs)
    return decorated_function



def admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        if not(session.get('user_type') == 'admin'):
            return render_template("pages/unauthorized.html")
            # return redirect('/login')
    
        return f(*args, **kwargs)
    return decorated_function
        