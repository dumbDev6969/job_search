import os
from datetime import datetime, timedelta

from flask import Flask, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sock import Sock
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
csrf = CSRFProtect(app)

from routes import *

socketio = init_socketio(app)
# Configure session
app.secret_key = os.environ.get("secret")
app.config["SESSION_TYPE"] = "filesystem"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)
app.config["UPLOAD_FOLDER"] = "files"

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[],
    storage_uri="memory://",
)
limiter.init_app(app)

print(app.url_map)
app.register_blueprint(routes_bp)

# Apply rate limiting to specific routes
# limiter.limit("5/minute")(login)
# limiter.limit("3/minute")(otp)
# limiter.limit("5/minute")(signup)


if __name__ == "__main__":
    try:
        socketio.run(app, debug=True, allow_unsafe_werkzeug=True)
    except ImportError as e:
        print(f"ImportError: {e}")
        print("Please ensure all required packages are installed.")
