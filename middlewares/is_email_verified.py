from flask import redirect, session, request,render_template
from functools import wraps
from utils.database import get_db
from sqlalchemy import text

def is_email_verified(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):

        db = get_db()
        email = session['email']
        verify_query = text("SELECT COUNT(*) as count FROM verified_users WHERE email = :email")
        verify_result = db.execute_query(verify_query, {'email': email})
        db.close()

        if not verify_result['success'] or verify_result['output'][0]['count'] == 0:
            return render_template("/auth/otp_virification.html",email=email),200
        
        return f(*args, **kwargs)
    return decorated_function
        