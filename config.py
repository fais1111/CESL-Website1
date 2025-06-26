import os
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SESSION_SECRET') or 'dev-secret-key-change-in-production'
    
    # Firebase configuration
    FIREBASE_API_KEY = os.environ.get('FIREBASE_API_KEY')
    FIREBASE_PROJECT_ID = os.environ.get('FIREBASE_PROJECT_ID')
    FIREBASE_APP_ID = os.environ.get('FIREBASE_APP_ID')
    
    # Admin credentials (store securely in production)
    ADMIN_USERNAME = os.environ.get('ADMIN_USERNAME')
    ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD')
    
    # Security settings
    SESSION_COOKIE_SECURE = os.environ.get('FLASK_ENV') == 'production'
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Deployment settings
    PREFERRED_URL_SCHEME = 'https' if os.environ.get('FLASK_ENV') == 'production' else 'http'

class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
    SESSION_COOKIE_SECURE = True

# Configuration selector
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}