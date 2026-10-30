from flask import request

def json_body():
    body = request.get_json(silent=True)  
    return body if isinstance(body, dict) else {}
