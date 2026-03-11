from datetime import datetime
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from extensions import db

bcrypt = Bcrypt()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='user')  # 'user' or 'owner'
    department = db.Column(db.String(100), default='')
    year = db.Column(db.String(20), default='')
    college = db.Column(db.String(200), default='')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    favourites = db.relationship('Favourite', backref='user', lazy=True)
    ratings = db.relationship('Rating', backref='user', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    @property
    def is_owner(self):
        return self.role == 'owner'
