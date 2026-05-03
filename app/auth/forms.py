from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=80)]
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Length(max=120), Email()]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired(), Length(min=8)]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match.")]
    )
    submit = SubmitField("Create Account")

    def validate_username(self, username):
        existing = User.query.filter_by(username=username.data.strip()).first()
        if existing:
            raise ValidationError("That username is already taken.")

    def validate_email(self, email):
        existing = User.query.filter_by(email=email.data.strip().lower()).first()
        if existing:
            raise ValidationError("That email is already registered.")


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Log In")
