from flask import Blueprint, request, render_template, jsonify, session,redirect
from utils.database import get_db
from utils.pasword_hash import verify_password
from utils.email_utils import check_email_exists
from utils.otp_utils import generate_otp,send_otp_email
from sqlalchemy import text
from datetime import datetime,timedelta

logout = Blueprint('logout', __name__)

@logout.route('/logout')
def logout_route():
    session.clear()
    return redirect('/login')