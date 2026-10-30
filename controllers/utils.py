from flask import request


def json_body():
    body = request.get_json(silent=True)  # None when missing or malformed
    return body if isinstance(body, dict) else {}
