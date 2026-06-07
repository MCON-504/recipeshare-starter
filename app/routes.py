import recipe
from dotenv import main
from flask import Blueprint, jsonify, request, render_template, flash, redirect, url_for, abort
from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange
from flask import render_template, redirect, url_for, flash
from .forms import FeedbackForm, ProfileForm, RecipeReviewForm
from app.forms import ProfileForm
from app.models import Profile, RecipeReview
from .extensions import db
from .models import Recipe

main_bp = Blueprint("main_bp", __name__)


@main_bp.route("/")
def api_home():
    return jsonify({"message": "RecipeShare API is running"})


@main_bp.route("/api/recipes", methods=["GET"])
def get_api_recipes():
    recipes = Recipe.query.order_by(Recipe.created_at.desc()).all()
    return jsonify([r.to_dict() for r in recipes]), 200

@main_bp.route("/recipes", methods = ["GET"])
def get_recipes():
    recipes = Recipe.query.order_by(Recipe.created_at.desc()).all()
    if request.is_json:
        return jsonify([recipee.to_dict() for recipee in recipes])
    return render_template("home.html", recipes = recipes)


@main_bp.route("/recipes/<int:recipe_id>", methods=["GET"])
def get_recipe(recipe_id: int):
    recipe = Recipe.query.get_or_404(recipe_id)
    if request.is_json:
        return jsonify(recipe.to_dict())
    else:
        return render_template("recipe_detail.html", recipe=recipe)


@main_bp.route("/recipes", methods=["POST"])
@login_required
def create_recipe():
    data = request.get_json() or {}

    required_fields = ["title", "description", "instructions", "prep_time"]
    missing = [field for field in required_fields if field not in data]
    if missing:
        return {"error": f"Missing required fields: {', '.join(missing)}"}, 400

    recipe = Recipe(
        title=data["title"],
        description=data["description"],
        instructions=data["instructions"],
        prep_time=data["prep_time"],
        author=current_user,
    )

    db.session.add(recipe)
    db.session.commit()

    return jsonify(recipe.to_dict()), 201


@main_bp.route("/recipes/<int:recipe_id>", methods=["PATCH"])
@login_required
def update_recipe(recipe_id: int):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != current_user.id:
        return jsonify({"error": "forbidden"}), 403

    data = request.get_json() or {}
    updatable_fields = ["title", "description", "instructions", "prep_time"]
    for field in updatable_fields:
        if field in data:
            setattr(recipe, field, data[field])

    db.session.commit()
    return jsonify(recipe.to_dict()), 200


@main_bp.route("/recipes/<int:recipe_id>", methods=["DELETE"])
@login_required
def delete_recipe(recipe_id: int):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != current_user.id:
        return jsonify({"error": "forbidden"}), 403
    db.session.delete(recipe)
    db.session.commit()
    return "", 204

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
        recipe = Recipe(
            title=form.title.data,
            description=form.description.data,
            instructions=form.instructions.data,
            prep_time=form.prep_time.data,
            author=current_user
        )
        db.session.add(recipe)
        db.session.commit()

        flash("Recipe created!", "success")
        return redirect(url_for("main_bp.get_recipe", recipe_id=recipe.id))


    # TODO: render the recipe_form.html template, passing the form

    return render_template("recipe_form.html", form = form)



@main_bp.route("/feedback", methods=["GET", "POST"])
def feedback():
    form = FeedbackForm()

    if form.validate_on_submit():
        flash(f"Thanks, {form.name.data}! We received your feedback.", "success")
        return redirect(url_for("main_bp.feedback"))

    return render_template("feedback.html", form=form)

@main_bp.route("/profile", methods = ["GET", "POST"])
@login_required
def profile():
    profile = current_user.profile
    form = ProfileForm(obj = profile)

    if form.validate_on_submit():
        if profile is None:
            profile = Profile(user = current_user)
            db.session.add(profile)

        profile.display_name = form.display_name.data.strip()
        profile.bio = form.bio.data
        profile.favorite_cuisine = form.favorite_cuisine.data.strip()
        profile.years_of_cooking = form.years_of_cooking.data

        db.session.commit()
        flash("Profile saved sucessfully.", "sucess")
        return redirect(url_for("main_bp.profile"))

    return render_template("profile_form.html", form = form)

@main_bp.route("/recipes/<int:recipe_id>/review", methods = ["GET", "POST"])
@login_required
def recipe_rating(recipe_id):
    recipe = db.session.get(Recipe, recipe_id)
    if not recipe:
        abort(404)
    form = RecipeReviewForm()

    if form.validate_on_submit():
        recipereview = RecipeReview()

        recipereview.rating = form.rating.data
        recipereview.comment = form.comment.data.strip()
        recipereview.recipe_id = recipe_id
        recipereview.user_id = current_user.id

        db.session.add(recipereview)
        db.session.commit()
        flash("Sucess!Welcome!")

        return redirect(url_for("main_bp.get_recipe", recipe_id = recipe.id))


    return render_template("review_form.html", form= form, recipe= recipe)





