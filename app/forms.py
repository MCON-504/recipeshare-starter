from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, Length


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

    from wtforms import IntegerField
from wtforms.validators import NumberRange


class RecipeForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[DataRequired(), Length(min=3, max=120)]
    )
    description = TextAreaField(
        "Description",
        validators=[DataRequired(), Length(min=10, max=300)]
    )
    instructions = TextAreaField(
        "Instructions",
        validators=[DataRequired(), Length(min=10)]
    )
    prep_time = IntegerField(
        "Prep Time in Minutes",
        validators=[DataRequired(), NumberRange(min=1, max=1440)]
    )
    submit = SubmitField("Create Recipe")