from flask import Blueprint, jsonify, request, render_template
from flask_login import login_required, current_user

from .extensions import db
from .models import Recipe

main_bp = Blueprint("main_bp", __name__)


@main_bp.route("/")
def api_home():
    return jsonify({"message": "RecipeShare API is running"})


@main_bp.route("/recipes", methods=["GET"])
def get_recipes():
    recipes = Recipe.query.order_by(Recipe.created_at.desc()).all()
    if request.is_json:
        return jsonify([recipe.to_dict() for recipe in recipes])
    return render_template("home.html", recipes=recipes)


@main_bp.route("/recipes/<int:recipe_id>", methods=["GET"])
def get_recipe(recipe_id: int):
    recipe = Recipe.query.get_or_404(recipe_id)
    return jsonify(recipe.to_dict())


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

