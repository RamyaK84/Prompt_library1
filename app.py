import os
from flask import Flask
from config import Config
from extensions import db, login_manager, bcrypt

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

    with app.app_context():
        db.create_all()
        seed_demo_users()

    return app

def seed_demo_users():
    from models.user import User
    from extensions import db
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

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
