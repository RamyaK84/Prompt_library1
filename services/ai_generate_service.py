import urllib.request
import urllib.error
import json

def generate_with_gemini(api_key, role, category, description, user_data=None):
    """Generate a custom prompt using Google Gemini API."""

    name = user_data.get('name', '[Your Name]') if user_data else '[Your Name]'
    department = user_data.get('department', '[Your Department]') if user_data else '[Your Department]'
    year = user_data.get('year', '[Your Year]') if user_data else '[Your Year]'
    college = user_data.get('college', '[Your College]') if user_data else '[Your College]'

    system_prompt = f"""You are an expert prompt engineer helping students and HR professionals.

Generate a high-quality, ready-to-use AI prompt based on the user's request.

User Details:
- Name: {name}
- Role: {role}
- Department: {department}
- Year: {year}
- College: {college}
- Category: {category}
- What they need: {description}

Rules:
1. Generate ONE complete, professional prompt they can directly use with any AI tool
2. If user details are provided (not placeholder), include them naturally in the prompt
3. Use [BRACKETS] for parts the user still needs to fill in
4. Make it detailed, specific, and professional
5. Format it clearly with line breaks
6. Do NOT add explanations before or after - just the prompt itself
7. Start the prompt directly, no intro text like "Here is your prompt:"
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"

    payload = {
        "contents": [{"parts": [{"text": system_prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 1024}
    }

    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})

    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            result = json.loads(response.read().decode('utf-8'))
            text = result['candidates'][0]['content']['parts'][0]['text']
            return {'success': True, 'prompt': text.strip()}
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        try:
            error_json = json.loads(error_body)
            msg = error_json.get('error', {}).get('message', 'API error')
        except:
            msg = f'HTTP {e.code} error'
        return {'success': False, 'error': msg}
    except Exception as e:
        return {'success': False, 'error': str(e)}
