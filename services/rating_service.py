from extensions import db
from models.rating import Rating

def rate_prompt(user_id, prompt_id, score):
    existing = Rating.query.filter_by(user_id=user_id, prompt_id=prompt_id).first()
    if existing:
        existing.score = score
    else:
        r = Rating(user_id=user_id, prompt_id=int(prompt_id), score=float(score))
        db.session.add(r)
    db.session.commit()

def get_prompt_rating(prompt_id):
    ratings = Rating.query.filter_by(prompt_id=int(prompt_id)).all()
    if not ratings:
        return None, 0
    avg = sum(r.score for r in ratings) / len(ratings)
    return round(avg, 1), len(ratings)

def get_user_rating(user_id, prompt_id):
    r = Rating.query.filter_by(user_id=user_id, prompt_id=int(prompt_id)).first()
    return r.score if r else None
