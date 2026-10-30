from flask import Flask

from config.config import CONFIGS
from extension import bcrypt, db, migrate


def create_app(env_name="development", overrides=None):
    app = Flask(__name__)
    app.config.from_object(CONFIGS[env_name])
    if overrides:
        app.config.update(overrides)

    db.init_app(app)  # connect extensions
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    # imported so Flask-Migrate can see the tables
    from models.note import Note  # noqa: F401
    from models.user import User  # noqa: F401

    return app
