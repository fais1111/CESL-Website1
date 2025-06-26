import os
from flask import Flask
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix
from config import config

# --- START: Firebase Admin Initialization ---
import json

cred_path = '/tmp/firebase-key.json'
json_str = os.environ.get('FIREBASE_SERVICE_ACCOUNT_JSON')

if json_str:
    with open(cred_path, 'w') as f:
        f.write(json_str)

    import firebase_admin
    from firebase_admin import credentials

    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(cred)
    print("Firebase initialized successfully.")
else:
    print("FIREBASE_SERVICE_ACCOUNT_JSON environment variable not set.")
# --- END: Firebase Admin Initialization ---

# Create the app with configuration
app = Flask(__name__)

# Load configuration based on environment
env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config.get(env, config['default']))

# Set secret key
app.secret_key = app.config['SECRET_KEY']

# Configure proxy fix for production
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Please log in to access the admin panel.'

@login_manager.user_loader
def load_user(user_id):
    from models import Admin
    return Admin.get(user_id)

# Security headers
@app.after_request
def security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    if app.config.get('SESSION_COOKIE_SECURE'):
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

# Import routes
from routes import *

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=app.config['DEBUG'])
