from extensions import db
from models.usage import Usage
from config import Config

def track_usage(prompt_id, user_id=None, session_id=None, action='copy'):
    u = Usage(prompt_id=int(prompt_id), user_id=user_id, session_id=session_id, action=action)
    db.session.add(u)
    db.session.commit()

def get_guest_usage_count(session_id):
    return Usage.query.filter_by(session_id=session_id, user_id=None).count()

def can_use_prompt(user_id, session_id):
    if user_id:
        return True
    count = get_guest_usage_count(session_id)
    return count < Config.GUEST_USAGE_LIMIT

def get_usage_analytics():
    from sqlalchemy import func
    results = db.session.query(Usage.prompt_id, func.count(Usage.id)).group_by(Usage.prompt_id).all()
    return {pid: count for pid, count in results}
