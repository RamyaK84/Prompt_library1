from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from extensions import db
from models.review import Review
from services.rating_service import rate_prompt

review_bp = Blueprint('review', __name__)

@review_bp.route('/api/review', methods=['POST'])
@login_required
def add_review():
    data = request.get_json()
    prompt_id = int(data.get('prompt_id'))
    content = data.get('content', '').strip()
    score = data.get('score')
    if not content:
        return jsonify({'success': False, 'message': 'Review cannot be empty'})
    review = Review(user_id=current_user.id, prompt_id=prompt_id, content=content)
    db.session.add(review)
    db.session.commit()
    if score:
        rate_prompt(current_user.id, prompt_id, float(score))
    return jsonify({'success': True, 'reviewer': current_user.name, 'content': content})

@review_bp.route('/api/reviews/<int:prompt_id>')
def get_reviews(prompt_id):
    reviews = Review.query.filter_by(prompt_id=prompt_id).order_by(Review.created_at.desc()).limit(10).all()
    from models.user import User
    result = []
    for r in reviews:
        user = User.query.get(r.user_id)
        result.append({'reviewer': user.name if user else 'User', 'content': r.content,
                      'date': r.created_at.strftime('%b %d, %Y')})
    return jsonify(result)

@review_bp.route('/api/rate', methods=['POST'])
@login_required
def rate():
    data = request.get_json()
    rate_prompt(current_user.id, int(data.get('prompt_id')), float(data.get('score')))
    return jsonify({'success': True})
