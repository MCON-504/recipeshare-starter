from flask import Flask, jsonify, render_template

from .config import Config
from .extensions import db, migrate, login_manager


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    migrate.init_app(app, db)

    # Flask-Login setup
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"
    login_manager.init_app(app)

    # ✅ FIX: prevent 302 redirects (this is what your tests need)
    @login_manager.unauthorized_handler
    def unauthorized():
        return jsonify({"error": "unauthorized"}), 401

    # register blueprints
    from .routes import main_bp
    app.register_blueprint(main_bp, url_prefix="/api")

    from .auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    from .models import Recipe

    @app.route("/")
    def home():
        recipes = Recipe.query.order_by(Recipe.created_at.desc()).all()
        return render_template("home.html", recipes=recipes)

    return app


# Flask-Login user loader
@login_manager.user_loader
def load_user(user_id: str):
    from .models import User
    return User.query.get(int(user_id))
