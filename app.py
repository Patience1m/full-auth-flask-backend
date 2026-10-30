from flask import Flask
from config.config import CONFIGS
from extension import bcrypt, db, migrate

def create_app(env_name="development", overrides=None):
    app = Flask(__name__)
    app.config.from_object(CONFIGS[env_name])
    if overrides:
        app.config.update(overrides)
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)
    from models.note import Note
    from models.user import User
    from controllers.auth_routes import auth_bp
    from controllers.note_routes import notes_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(notes_bp)

    return app
