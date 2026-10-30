from flask import Blueprint, g, jsonify, request
from controllers.utils import json_body
from models.note import Note
from services.auth import login_required
from services.service import fetch, paginate, remove, save, update  

notes_bp = Blueprint("notes", __name__)

DEFAULT_PER_PAGE = 5
MAX_PER_PAGE = 50

def get_owned_note(pk): 
    note = fetch(Note, pk)
    if note is None:
        return None, (jsonify({"errors": ["Note not found."]}), 404)
    if note.user_id != g.user.id:
        return None, (jsonify({"errors": ["You can only access your own notes."]}), 403)
    return note, None

@notes_bp.route("/notes", methods=["GET"])
@login_required
def list_notes_handler():
    page = max(request.args.get("page", 1, type=int), 1)
    per_page = request.args.get("per_page", DEFAULT_PER_PAGE, type=int)
    per_page = min(max(per_page, 1), MAX_PER_PAGE)
    result = paginate(Note, page, per_page, user_id=g.user.id)  
    return jsonify({
        "page": result.page,
        "per_page": result.per_page,
        "total": result.total,
        "pages": result.pages,
        "notes": [note.to_dict() for note in result.items],
    }), 200

@notes_bp.route("/notes/<int:pk>", methods=["GET"])
@login_required
def read_note_handler(pk):
    note, failure = get_owned_note(pk)
    if failure:
        return failure
    return jsonify(note.to_dict()), 200

@notes_bp.route("/notes", methods=["POST"])
@login_required
def create_note_handler():
    body = json_body()
    try:
        note = Note(
            title=body.get("title"),
            content=body.get("content"),
            user_id=g.user.id,  
        )
        save(note)
    except ValueError as err:  
        return jsonify({"errors": [str(err)]}), 422
    return jsonify(note.to_dict()), 201

@notes_bp.route("/notes/<int:pk>", methods=["PATCH"])
@login_required
def update_note_handler(pk):
    note, failure = get_owned_note(pk)
    if failure:
        return failure
    body = json_body()
    changes = {key: body[key] for key in ("title", "content") if key in body}
    if not changes:
        return jsonify({"errors": ["Provide a title and/or content to update."]}), 422
    try:
        update(note, **changes)
    except ValueError as err:
        return jsonify({"errors": [str(err)]}), 422
    return jsonify(note.to_dict()), 200

@notes_bp.route("/notes/<int:pk>", methods=["DELETE"])
@login_required
def delete_note_handler(pk):
    note, failure = get_owned_note(pk)
    if failure:
        return failure
    remove(note)
    return "", 204
