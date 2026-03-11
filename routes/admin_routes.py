from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from services.usage_service import get_usage_analytics
from models.review import Review
from models.user import User
from extensions import db
from utils.prompt_loader import load_prompts

admin_bp = Blueprint('admin', __name__)

def owner_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_owner:
            flash('Access denied. Owner account required.', 'error')
            return redirect(url_for('prompt.index'))
        return f(*args, **kwargs)
    return decorated

@admin_bp.route('/admin')
@login_required
@owner_required
def dashboard():
    analytics = get_usage_analytics()
    prompts = load_prompts()
    users = User.query.all()
    reviews = Review.query.order_by(Review.created_at.desc()).limit(20).all()
    prompt_map = {p['id']: p['title'] for p in prompts}
    user_map = {u.id: u.name for u in users}
    return render_template('admin_dashboard.html', analytics=analytics, prompts=prompts,
                           users=users, reviews=reviews, prompt_map=prompt_map, user_map=user_map)

@admin_bp.route('/admin/delete-review/<int:review_id>', methods=['POST'])
@login_required
@owner_required
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    db.session.delete(review)
    db.session.commit()
    flash('Review deleted.', 'success')
    return redirect(url_for('admin.dashboard'))
