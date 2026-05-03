from flask import request, jsonify, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required

from app.extensions import db
from app.models import User
from .forms import RegistrationForm, LoginForm
from . import auth_bp


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    # ── JSON / API path ──────────────────────────────────────────────────
    if request.is_json:
        data     = request.get_json() or {}
        username = data.get("username", "").strip()
        email    = data.get("email",    "").strip().lower()
        password = data.get("password", "")

        if not username or not email or not password:
            return jsonify({"error": "username, email and password are required"}), 400
        if len(password) < 8:
            return jsonify({"error": "password must be at least 8 characters"}), 400
        if User.query.filter_by(username=username).first():
            return jsonify({"error": "username already taken"}), 409
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "email already registered"}), 409

        user = User(username=username, email=email)
        user.password = password
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict()), 201

    # ── HTML form path ───────────────────────────────────────────────────
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data.strip(),
            email=form.email.data.strip().lower()
        )
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html", form=form)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    # ── JSON / API path ──────────────────────────────────────────────────────
    if request.is_json:
        data     = request.get_json() or {}
        username = data.get("username", "")
        password = data.get("password", "")

        user = User.query.filter_by(username=username).first()
        if user is None or not user.verify_password(password):
            return jsonify({"error": "invalid username or password"}), 401

        remember = data.get("remember_me", False)
        login_user(user, remember=remember)
        return jsonify(user.to_dict()), 200

    # ── HTML form path ───────────────────────────────────────────────────────
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash("Invalid username or password.", "danger")
            return render_template("auth/login.html", form=form), 401

        login_user(user, remember=form.remember_me.data)
        flash(f"Welcome back, {user.username}! You are now logged in.", "success")
        return redirect(url_for("main_bp.get_recipes"))

    return render_template("auth/login.html", form=form)


@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "logged out"}), 200
