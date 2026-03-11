from extensions import db
from models.favourite import Favourite

def add_favourite(user_id, prompt_id):
    existing = Favourite.query.filter_by(user_id=user_id, prompt_id=prompt_id).first()
    if existing:
        return False
    fav = Favourite(user_id=user_id, prompt_id=int(prompt_id))
    db.session.add(fav)
    db.session.commit()
    return True

def remove_favourite(user_id, prompt_id):
    fav = Favourite.query.filter_by(user_id=user_id, prompt_id=prompt_id).first()
    if fav:
        db.session.delete(fav)
        db.session.commit()
        return True
    return False

def get_user_favourites(user_id):
    favs = Favourite.query.filter_by(user_id=user_id).all()
    return [f.prompt_id for f in favs]

def is_favourite(user_id, prompt_id):
    return Favourite.query.filter_by(user_id=user_id, prompt_id=int(prompt_id)).first() is not None
