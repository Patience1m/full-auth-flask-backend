from sqlalchemy.orm import validates

from extension import bcrypt, db


class User(db.Model):
    __tablename__ = "users"  # Always explicit

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)  # never the plain password

    # one user owns many notes; deleting the user deletes their notes
    notes = db.relationship(
        "Note",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    @validates("username")
    def validate_username(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Username is required.")
        value = value.strip()
        if len(value) > 50:
            raise ValueError("Username must be 50 characters or fewer.")
        return value

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.id}: {self.username}>"

    def to_dict(self):
        return {"id": self.id, "username": self.username}  # the hash is never exposed
