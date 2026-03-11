from flask import Blueprint, request, jsonify
from flask_login import current_user
from services.ai_generate_service import generate_with_gemini

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/api/ai-generate', methods=['POST'])
def ai_generate():
    data = request.get_json()
    api_key = data.get('api_key', '').strip()
    role = data.get('role', 'student')
    category = data.get('category', '')
    description = data.get('description', '').strip()

    if not api_key:
        return jsonify({'success': False, 'error': 'Please enter your Gemini API key.'})
    if not description:
        return jsonify({'success': False, 'error': 'Please describe what you need.'})

    user_data = None
    if current_user.is_authenticated:
        user_data = {
            'name': current_user.name,
            'department': current_user.department or '',
            'year': current_user.year or '',
            'college': current_user.college or ''
        }

    result = generate_with_gemini(api_key, role, category, description, user_data)
    return jsonify(result)
