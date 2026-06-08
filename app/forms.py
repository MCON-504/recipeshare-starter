# Homework 2 — Starter snippet for app/routes.py
#
# Add the RecipeForm class and the two new route functions to app/routes.py.
# The existing routes (get_recipes, get_recipe, create_recipe, …) are UNCHANGED.
#
# Steps:
#   1. Add the missing imports at the top of routes.py
#   2. Complete the RecipeForm field definitions
#   3. Implement new_recipe() — GET renders the blank form, POST saves to db

# ── Additional imports to add at the top of routes.py ─────────────────────────
from flask import render_template, flash, redirect, url_for  # already partly imported
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Email
from flask import Blueprint, jsonify, request, render_template
from flask_login import login_required, current_user

from .extensions import db
from .models import Recipe


# ── Form class ─────────────────────────────────────────────────────────────────
class RecipeForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[DataRequired(), Length(max=150)]
    )
    description = TextAreaField(
        "Description",
        validators=[DataRequired()]
    )
    instructions = TextAreaField(
        "Instructions",
        validators=[DataRequired()]
    )
    prep_time = IntegerField(
        "Prep Time (minutes)",
        validators=[DataRequired(), NumberRange(min=1)]
    )
    submit = SubmitField("Save Recipe")



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
        "Comment", validators=[DataRequired(), Length(max=300)]
    )


    submit = SubmitField("Save Review")

