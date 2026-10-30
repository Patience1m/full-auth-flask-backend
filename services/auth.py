from functools import wraps

from flask import g, jsonify, session

from models.user import User
from services.service import fetch


def current_user():
    user_id = session.get("user_id")
    if user_id is None:
        return None
    return fetch(User, user_id)  # None if the account no longer exists


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        user = current_user()
        if user is None:
            return jsonify({"errors": ["Unauthorized"]}), 401
        g.user = user  # handlers read the logged-in user from here
        return view(*args, **kwargs)

    return wrapped_view
