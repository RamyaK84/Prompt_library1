from flask import Blueprint, render_template, request, jsonify
from services.search_service import keyword_search
from services.semantic_search_service import semantic_search

search_bp = Blueprint('search', __name__)

@search_bp.route('/search')
def search():
    query = request.args.get('q', '')
    mode = request.args.get('mode', 'keyword')
    category = request.args.get('category', '')
    results = []
    if query:
        if mode == 'smart':
            results = semantic_search(query)
        else:
            results = keyword_search(query, category if category else None)
    return render_template('search.html', results=results, query=query, mode=mode, category=category)

@search_bp.route('/api/search')
def api_search():
    query = request.args.get('q', '')
    mode = request.args.get('mode', 'keyword')
    if not query:
        return jsonify([])
    if mode == 'smart':
        results = semantic_search(query, top_k=5)
    else:
        results = keyword_search(query)[:5]
    return jsonify(results)
