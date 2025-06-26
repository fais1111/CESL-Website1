import os
from flask import Flask
from flask_login import LoginManager
from werkzeug.middleware.proxy_fix import ProxyFix
from config import config, Config

# Create Flask app
app = Flask(__name__)

# Load env config
env = os.environ.get('FLASK_ENV')
app.config.from_object(config.get(env, config['default']))

# Initialize Firebase
Config.init_firebase()

# Set Flask secret
app.secret_key = app.config['SECRET_KEY']

# Middleware for proxy
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Please log in to access the admin panel.'

@login_manager.user_loader
def load_user(user_id):
    from models import Admin
    return Admin.get(user_id)

# Set security headers
@app.after_request
def security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    if app.config.get('SESSION_COOKIE_SECURE'):
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

# Load routes
from routes import *

# Run server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])
