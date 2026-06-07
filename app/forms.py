from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.fields.choices import SelectField
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange


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
    display_name = StringField("name", validators = [DataRequired(), Length(2, 80)])
    bio = TextAreaField("bio", validators = [Optional(), Length(0, 300)])
    favorite_cuisine = StringField("favorite cuisine", validators = [Optional(), Length(0, 80)])
    years_of_cooking = IntegerField("years of cooking", validators = [Optional(), NumberRange(0,100)])
    submit = SubmitField("Save Profile")

class RecipeReviewForm(FlaskForm):
    rating = SelectField("Rating", validators = [DataRequired()], choices = [(1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5")])
    comment = TextAreaField("Comment", validators = [DataRequired(), Length(5, 300)])
    submit = SubmitField("Submit Review")