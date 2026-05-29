from datetime import datetime, UTC

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db


class User(UserMixin, db.Model):
    __tablename__ = "users"

    id            = db.Column(db.Integer, primary_key=True)
    username      = db.Column(db.String(80),  nullable=False, unique=True)
    email         = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=True)

    recipes = db.relationship("Recipe", back_populates="author", lazy=True)

    # ── password property (write-only) ──────────────────
    @property
    def password(self):
        raise AttributeError("password is write-only")

    @password.setter
    def password(self, raw_password: str):
        self.password_hash = generate_password_hash(raw_password)

    # ── verify_password ──────────────────────────────────
    def verify_password(self, raw_password: str) -> bool:
        return check_password_hash(self.password_hash, raw_password)

    # ── to_dict (excludes hash for safety) ──────────────
    def to_dict(self) -> dict:
        return {
            "id":       self.id,
            "username": self.username,
            "email":    self.email,
        }


class Recipe(db.Model):
    __tablename__ = "recipes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    prep_time = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(UTC), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    author = db.relationship("User", back_populates="recipes")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "instructions": self.instructions,
            "prep_time": self.prep_time,
            "created_at": self.created_at.isoformat(),
            "user_id": self.user_id,
        }
class Profile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    display_name = db.Column(db.String(80), nullable=False)
    bio = db.Column(db.String(300))
    favorite_cuisine = db.Column(db.String(80))
    years_cooking = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    user = db.relationship("User", backref=db.backref("profile", uselist=False))

