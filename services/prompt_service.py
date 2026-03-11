from utils.prompt_loader import load_prompts, get_prompt_by_id, get_categories
from utils.placeholder_replacer import replace_placeholders

def get_all_prompts(category=None, subcategory=None):
    prompts = load_prompts()
    if subcategory:
        prompts = [p for p in prompts if p.get('subcategory') == subcategory]
    if category:
        prompts = [p for p in prompts if p.get('category') == category]
    return prompts

def get_prompt(prompt_id):
    return get_prompt_by_id(prompt_id)

def get_personalized_prompt(prompt_id, user):
    prompt = get_prompt_by_id(prompt_id)
    if not prompt:
        return None
    user_data = {
        'name': getattr(user, 'name', ''),
        'department': getattr(user, 'department', ''),
        'year': getattr(user, 'year', ''),
        'college': getattr(user, 'college', '')
    }
    personalized = dict(prompt)
    personalized['template'] = replace_placeholders(prompt['template'], user_data)
    return personalized

def get_all_categories():
    return get_categories()

def match_best_template(role, category, description):
    prompts = load_prompts()
    filtered = [p for p in prompts if p.get('role', '').lower() == role.lower() or p.get('category', '').lower() == category.lower()]
    if not filtered:
        filtered = prompts
    # simple keyword match
    desc_lower = description.lower()
    scored = []
    for p in filtered:
        score = sum(1 for tag in p.get('tags', []) if tag.lower() in desc_lower)
        scored.append((score, p))
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[0][1] if scored else filtered[0]
