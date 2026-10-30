import os


class BaseConfig:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # signs the session cookie, so set a real value outside development
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-secret-key")


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///productivity.db"  # lands in instance/


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


CONFIGS = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
}
