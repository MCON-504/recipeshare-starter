from flask import Blueprint, jsonify, request, render_template
from flask_login import login_required, current_user
#from forms import RecipeForm
from .extensions import db
from .models import Recipe,Profile, RecipeReview
from flask import render_template, flash, redirect, url_for  # already partly imported
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange
from .forms import FeedbackForm, ProfileForm, RecipeForm, RecipeReviewForm

main_bp = Blueprint("main_bp", __name__)

@main_bp.route("/")
def api_home():
    return jsonify({"message": "RecipeShare API is running"})


@main_bp.route("/recipes", methods=["GET"])
def get_recipes():
    recipes = Recipe.query.order_by(Recipe.created_at.desc()).all()
    if request.is_json :
        return jsonify([recipe.to_dict() for recipe in recipes])
    return render_template("home.html", recipes=recipes)

@main_bp.route("/recipes/<int:recipe_id>", methods=["GET"])
def get_recipe(recipe_id: int):
    recipe = Recipe.query.get_or_404(recipe_id)
    reviews = RecipeReview.query.filter_by(recipe_id = recipe_id)
    if request.is_json :
        return jsonify(recipe.to_dict())
    return render_template("recipe_detail.html", recipe=recipe, reviews=reviews)




@main_bp.route("/recipes", methods=["POST"])
@login_required
def create_recipe():
    if request.is_json:
        data = request.get_json() or {}
    else:
        data = request.form.to_dict()

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
    if request.is_json:
        return jsonify(recipe.to_dict()), 201
    else:
        flash("Recipe created!", "success")
        return redirect(url_for("main_bp.get_recipe", recipe_id=recipe.id))



# ── New route ──────────────────────────────────────────────────────────────────
@main_bp.route("/recipes/new", methods=["GET", "POST"])
@login_required
def new_recipe():
    form = RecipeForm()

    if form.validate_on_submit():
        # TODO: create a Recipe from form data and save it
        recipe = Recipe(
                    title=form.title.data,
                    description=form.description.data,
                    instructions=form.instructions.data,
                    prep_time=form.prep_time.data,
                    author=current_user,)
        db.session.add(recipe)
        db.session.commit()
        flash("Recipe created!", "success")
        return redirect(url_for("main_bp.get_recipe", recipe_id=recipe.id))


    # TODO: render the recipe_form.html template, passing the form
    return render_template("recipe_form.html", form=form)



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
    form = ProfileForm(obj=profile)

    if form.validate_on_submit():
        if profile is None:
            profile = Profile(user=current_user)
            db.session.add(profile)

        profile.display_name = form.display_name.data.strip()
        profile.bio = (form.bio.data or "").strip() or None
        profile.favorite_cuisine = (form.favorite_cuisine.data or "").strip() or None
        profile.years_cooking = form.years_cooking.data

        db.session.commit()
        flash("Profile saved successfully", "success")
        return redirect(url_for("main_bp.profile"))

    return render_template("profile_form.html", form=form)

@main_bp.route("/recipes/<recipe_id>/review", methods = ["GET", "POST"])
@login_required
def review(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    form = RecipeReviewForm()

    if form.validate_on_submit():
        reviews = RecipeReview()


        reviews.rating = form.rating.data
        reviews.comment = (form.comment.data or "").strip() or None
        reviews.recipe_id = recipe.id
        reviews.user_id = current_user.id
        db.session.add(reviews)

        db.session.commit()
        flash("Thanks for your feedback!", "success")
        return redirect(url_for("main_bp.get_recipe", recipe_id=recipe_id))

    return render_template("review_form.html", form=form, recipe=recipe)
