import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Ensure required folders exist on the server
for folder in ['database', 'data']:
    os.makedirs(os.path.join(BASE_DIR, folder), exist_ok=True)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # Updated to work on Render's Linux environment
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(BASE_DIR, 'database', 'db.sqlite3')
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PROMPTS_FILE = os.path.join(BASE_DIR, 'data', 'prompts.json')
    GUEST_USAGE_LIMIT = 5
