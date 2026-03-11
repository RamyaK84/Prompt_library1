def replace_placeholders(template, user_data):
    result = template
    for key, value in user_data.items():
        if value:
            result = result.replace('{{' + key + '}}', str(value))
    return result
