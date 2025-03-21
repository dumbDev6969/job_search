from flask import Flask,request
from datetime import datetime,timedelta
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
from routes import *

# Configure session
app.secret_key = os.environ.get('secret')
app.config['SESSION_TYPE'] = 'filesystem'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)
limiter.init_app(app)


app.register_blueprint(routes_bp)
# Apply rate limiting to specific routes
limiter.limit("5/minute")(login)
limiter.limit("3/minute")(otp)
limiter.limit("5/minute")(signup)
if __name__ == '__main__':
    app.run(debug=True)