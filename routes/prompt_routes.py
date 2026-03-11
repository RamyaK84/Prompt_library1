from flask import Blueprint, render_template, request, jsonify, session
from flask_login import current_user
from services.prompt_service import get_all_prompts, get_prompt, get_personalized_prompt, get_all_categories, match_best_template
from services.favourite_service import get_user_favourites, is_favourite
from services.rating_service import get_prompt_rating, get_user_rating
from services.usage_service import track_usage, can_use_prompt
from utils.placeholder_replacer import replace_placeholders

prompt_bp = Blueprint('prompt', __name__)

@prompt_bp.route('/')
def index():
    prompts = get_all_prompts()[:6]
    categories = get_all_categories()
    fav_ids = get_user_favourites(current_user.id) if current_user.is_authenticated else []
    return render_template('index.html', prompts=prompts, categories=categories, fav_ids=fav_ids)

@prompt_bp.route('/prompts')
def prompts():
    category = request.args.get('category')
    subcategory = request.args.get('subcategory')
    all_prompts = get_all_prompts(category=category, subcategory=subcategory)
    categories = get_all_categories()
    fav_ids = get_user_favourites(current_user.id) if current_user.is_authenticated else []
    return render_template('prompts.html', prompts=all_prompts, categories=categories,
                           selected_category=category, selected_sub=subcategory, fav_ids=fav_ids)

@prompt_bp.route('/prompt/<int:prompt_id>')
def prompt_detail(prompt_id):
    if current_user.is_authenticated:
        p = get_personalized_prompt(prompt_id, current_user)
    else:
        p = get_prompt(prompt_id)
    if not p:
        return "Prompt not found", 404
    db_rating, count = get_prompt_rating(prompt_id)
    display_rating = db_rating if db_rating else p.get('rating', 4.0)
    user_rating = get_user_rating(current_user.id, prompt_id) if current_user.is_authenticated else None
    fav = is_favourite(current_user.id, prompt_id) if current_user.is_authenticated else False
    return render_template('prompt_detail.html', prompt=p, rating=display_rating,
                           rating_count=count, user_rating=user_rating, is_favourite=fav)

@prompt_bp.route('/api/use-prompt', methods=['POST'])
def use_prompt():
    data = request.get_json()
    prompt_id = data.get('prompt_id')
    sid = session.get('session_id', str(id(session)))
    session['session_id'] = sid
    user_id = current_user.id if current_user.is_authenticated else None
    if not can_use_prompt(user_id, sid):
        return jsonify({'success': False, 'message': 'Guest usage limit reached. Please login for unlimited access.', 'limit_reached': True})
    track_usage(prompt_id, user_id=user_id, session_id=sid)
    return jsonify({'success': True})

@prompt_bp.route('/personalize', methods=['GET', 'POST'])
def personalize():
    categories = get_all_categories()
    result = None
    if request.method == 'POST':
        role = request.form.get('role', 'student')
        category = request.form.get('category', '')
        description = request.form.get('description', '')
        template = match_best_template(role, category, description)
        user_data = {}
        if current_user.is_authenticated:
            user_data = {'name': current_user.name, 'department': current_user.department,
                        'year': current_user.year, 'college': current_user.college}
        result = dict(template)
        result['template'] = replace_placeholders(template['template'], user_data)
    return render_template('personalize.html', categories=categories, result=result)
