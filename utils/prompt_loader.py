import json
import os
from config import Config

_prompts_cache = None

def load_prompts():
    global _prompts_cache
    if _prompts_cache is None:
        with open(Config.PROMPTS_FILE, 'r', encoding='utf-8') as f:
            _prompts_cache = json.load(f)
    return _prompts_cache

def get_prompt_by_id(prompt_id):
    prompts = load_prompts()
    for p in prompts:
        if p['id'] == int(prompt_id):
            return p
    return None

def get_categories():
    prompts = load_prompts()
    categories = {}
    for p in prompts:
        sub = p.get('subcategory', 'Other')
        cat = p.get('category', 'Other')
        if sub not in categories:
            categories[sub] = set()
        categories[sub].add(cat)
    return {k: list(v) for k, v in categories.items()}
