from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from services.favourite_service import add_favourite, remove_favourite, get_user_favourites
from utils.prompt_loader import get_prompt_by_id

favourite_bp = Blueprint('favourite', __name__)

@favourite_bp.route('/favourites')
@login_required
def favourites():
    fav_ids = get_user_favourites(current_user.id)
    prompts = [get_prompt_by_id(pid) for pid in fav_ids]
    prompts = [p for p in prompts if p]
    return render_template('favourites.html', prompts=prompts, fav_ids=fav_ids)

@favourite_bp.route('/api/favourite', methods=['POST'])
@login_required
def toggle_favourite():
    data = request.get_json()
    prompt_id = data.get('prompt_id')
    fav_ids = get_user_favourites(current_user.id)
    if int(prompt_id) in fav_ids:
        remove_favourite(current_user.id, prompt_id)
        return jsonify({'status': 'removed'})
    else:
        add_favourite(current_user.id, prompt_id)
        return jsonify({'status': 'added'})
