from sqlalchemy.orm import validates

from extension import db


class Note(db.Model):
    __tablename__ = "notes"  # Always explicit

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False)

    # relationship column: every note belongs to exactly one user
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="notes")

    @validates("title", "content")
    def validate_text(self, key, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"{key.capitalize()} is required.")
        value = value.strip()
        if key == "title" and len(value) > 100:
            raise ValueError("Title must be 100 characters or fewer.")
        return value

    def __repr__(self):
        return f"<Note {self.id}: {self.title}>"

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "user_id": self.user_id,
        }
