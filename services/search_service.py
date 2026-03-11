from utils.prompt_loader import load_prompts

def keyword_search(query, category=None):
    prompts = load_prompts()
    query_lower = query.lower()
    results = []
    for p in prompts:
        searchable = f"{p['title']} {p['category']} {p['preview']} {' '.join(p.get('tags', []))}".lower()
        if query_lower in searchable:
            results.append(p)
    if category:
        results = [r for r in results if r.get('category') == category or r.get('subcategory') == category]
    return results
