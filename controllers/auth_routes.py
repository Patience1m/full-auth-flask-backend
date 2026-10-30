from flask import Blueprint, jsonify, session
from sqlalchemy.exc import IntegrityError
from controllers.utils import json_body
from models.user import User
from services.auth import current_user
from services.service import fetch_by, save 

auth_bp = Blueprint("auth", __name__)

MIN_PASSWORD_LENGTH = 6

@auth_bp.route("/signup", methods=["POST"])
def signup_handler():
    body = json_body()
    username = body.get("username")
    password = body.get("password")
    confirmation = body.get("password_confirmation")
    errors = []
    if not isinstance(username, str) or not username.strip():
        errors.append("Username is required.")
    elif fetch_by(User, username=username.strip()):
        errors.append("Username is already taken.")
    if not isinstance(password, str) or len(password) < MIN_PASSWORD_LENGTH:
        errors.append(f"Password must be at least {MIN_PASSWORD_LENGTH} characters.")
    elif confirmation is not None and confirmation != password:
        errors.append("Password and confirmation do not match.")
    if errors:
        return jsonify({"errors": errors}), 422
    try:
        user = User(username=username.strip())
        user.set_password(password)
        save(user)
    except ValueError as err: 
        return jsonify({"errors": [str(err)]}), 422
    except IntegrityError:  
        return jsonify({"errors": ["Username is already taken."]}), 422
    session["user_id"] = user.id  
    return jsonify(user.to_dict()), 201

@auth_bp.route("/login", methods=["POST"])
def login_handler():
    body = json_body()
    username = body.get("username")
    password = body.get("password")
    user = None
    if isinstance(username, str) and isinstance(password, str):
        user = fetch_by(User, username=username.strip()) 
    if user is None or not user.check_password(password):
        return jsonify({"errors": ["Invalid username or password."]}), 401
    session["user_id"] = user.id
    return jsonify(user.to_dict()), 200

@auth_bp.route("/check_session", methods=["GET"])
def check_session_handler():
    user = current_user()
    if user is None:
        return jsonify({"errors": ["Unauthorized"]}), 401
    return jsonify(user.to_dict()), 200

@auth_bp.route("/logout", methods=["DELETE"])
def logout_handler():
    session.pop("user_id", None) 
    return "", 204
