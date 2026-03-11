from flask import Blueprint, render_template
from services.prompt_service import get_all_categories, get_all_prompts

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/categories')
def categories():
    cats = get_all_categories()
    prompts = get_all_prompts()
    return render_template('categories.html', categories=cats, prompts=prompts)
