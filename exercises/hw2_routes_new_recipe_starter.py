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
from wtforms.validators import DataRequired, Length, NumberRange


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


# ── New route ──────────────────────────────────────────────────────────────────
@main_bp.route("/recipes/new", methods=["GET", "POST"])
@login_required
def new_recipe():
    form = RecipeForm()

    if form.validate_on_submit():
        # TODO: create a Recipe from form data and save it
        #   recipe = Recipe(
        #       title=...,
        #       description=...,
        #       instructions=...,
        #       prep_time=...,
        #       author=current_user,
        #   )
        #   db.session.add(recipe)
        #   db.session.commit()
        #   flash("Recipe created!", "success")
        #   return redirect(url_for("main_bp.get_recipe", recipe_id=recipe.id))
        pass

    # TODO: render the recipe_form.html template, passing the form
    pass

