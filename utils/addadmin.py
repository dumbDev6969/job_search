from pasword_hash import hash_password
from flask import Blueprint, jsonify, render_template, request, redirect, url_for, session
from database import get_db
from sqlalchemy import text
def signup_admin(): 
    password_hash = hash_password("admin123")
    print(password_hash)
    try:
        # Get database connection
        db = get_db()
        
        # Insert employer data
        query = text("""
            INSERT INTO admin 
            (username, email, password)
            VALUES 
            (:username, :email, :password)
        """)
        
        result = db.execute_query(query, {
            'username': 'jem',
            'email': 'jem@admin.com',
            'password': password_hash,
           
        })
        
        if result['success']:
          
            return "success"
        else:
            return "fail"
            
    except Exception as e:
        return str(e)

a = signup_admin()
print(a)
            