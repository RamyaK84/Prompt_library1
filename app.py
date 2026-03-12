import os
import logging
from flask import Flask
from config import Config
from extensions import db, login_manager, bcrypt

# Set up logging to see errors in Render Logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'

    from models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Blueprint Registrations
    from routes.auth_routes import auth_bp
    from routes.prompt_routes import prompt_bp
    from routes.search_routes import search_bp
    from routes.favourite_routes import favourite_bp
    from routes.review_routes import review_bp
    from routes.profile_routes import profile_bp
    from routes.admin_routes import admin_bp
    from routes.categories_routes import categories_bp
    from routes.ai_routes import ai_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(prompt_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(favourite_bp)
    app.register_blueprint(review_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(ai_bp)

    # Database setup with error handling to prevent startup crashes
    with app.app_context():
        try:
            logger.info("Initializing database...")
            db.create_all()
            seed_demo_users()
            logger.info("Database initialized successfully.")
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            # We don't exit here so the app can still try to bind to the port

    return app

def seed_demo_users():
    from models.user import User
    from extensions import db
    try:
        if not User.query.filter_by(email='admin@demo.com').first():
            owner = User(name='Admin Owner', email='admin@demo.com', role='owner',
                        department='Computer Science', year='4', college='Demo College')
            owner.set_password('admin123')
            db.session.add(owner)
        if not User.query.filter_by(email='student@demo.com').first():
            student = User(name='Demo Student', email='student@demo.com', role='user',
                          department='Information Technology', year='3', college='Demo College')
            student.set_password('student123')
            db.session.add(student)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logger.error(f"Seeding failed: {e}")

# Create the app object for Gunicorn
app = create_app()

if __name__ == '__main__':
    # Bind to 0.0.0.0 and use Render's dynamic port
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
