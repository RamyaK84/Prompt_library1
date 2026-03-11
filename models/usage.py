from datetime import datetime
from extensions import db

class Usage(db.Model):
    __tablename__ = 'usage'
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    prompt_id = db.Column(db.Integer, nullable=False)
    action = db.Column(db.String(50), default='copy')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
