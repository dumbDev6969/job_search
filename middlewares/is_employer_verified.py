from flask import redirect, session, request,render_template
from functools import wraps
from utils.check_if_exists import check_column_exists
from utils.database import get_db
def is_employer_verified(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' in session:
            if  check_column_exists('employer', 'user_id', session['user_id']):
                logging.info(f"Checking if employer with id {session['user_id']} is verified")
                if not check_column_exists('employer_verification', 'employer_id', session['user_id']):
                    logging.info(f"Employer with id {session['user_id']} is not verified")
                    return redirect('/signup/employer/requirements')
                db= get_db()
                sql = f"SELECT * FROM employer_verification WHERE employer_id  = :employer_id AND status = :status"
                result = db.execute_query(sql, {'employer_id': session['user_id'], 'status': 'approved'})
                if result:
                    logging.info(f"Employer with id {session['user_id']} is verified")
                else:
                    logging.info(f"Employer with id {session['user_id']} is not verified")
                return result
               
        return f(*args, **kwargs)
    return decorated_function