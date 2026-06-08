from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, NumberRange

from app.models import User


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", # label
        validators=[DataRequired(), Length(min=3, max=80)] # validators - us shld validate all input
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

class FeedbackForm(FlaskForm):
    name = StringField(
       "Name",
        validators=[DataRequired(), Length(min=2, max=80)]
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email(), Length(max=120)]
    )
    topic = StringField(
        "Topic",
        validators=[DataRequired(), Length(max=100)]
    )
    message = TextAreaField(
        "Message",
        validators=[DataRequired(), Length(min=10, max=500)]
    )
    submit = SubmitField("Send Feedback")

class ProfileForm(FlaskForm):
    display_name = StringField(
        "Name", validators=[DataRequired(),Length(min=2, max=80)]
    )

    bio = TextAreaField(
        "bio", validators=[Length(max=300)]
    )

    favorite_cuisine = StringField("Favorite Cuisine", validators=[Length(max=800)])

    years_cooking = IntegerField("Years Cooking", validators=[NumberRange(min=0, max=100)])
    submit = SubmitField("Save Profile")

class RecipeReviewForm(FlaskForm):
    rating = IntegerField(
        "Rating", validators=[DataRequired(),NumberRange(min=1, max=5)]
    )

    comment = TextAreaField(
        "Comment", validators=[DataRequired(), Length(min=5, max=300)]
    )

    submit = SubmitField("Save Review")


