# Homework 1 — Starter snippet for app/auth/views.py
#
# Replace the existing `login` route's HTML form path with this version.
# The JSON path above it is UNCHANGED — do not touch it.
#
# Steps:
#   1. Import is_safe_url (helper provided below) at the top of views.py
#   2. After login_user(), call is_safe_url() on request.args.get("next")
#   3. Redirect to `next` if safe, otherwise to "main_bp.get_recipes"

from urllib.parse import urlparse


# ── Helper ────────────────────────────────────────────────────────────────────
def is_safe_url(target: str) -> bool:
    """Return True only for relative paths like /recipes/new.
    Rejects empty strings, external URLs (https://evil.com),
    and protocol-relative URLs (//evil.com).
    """
    # TODO: implement using urlparse
    #   hint: a safe URL has no netloc and its path starts with "/"
    pass


# ── Login route (HTML form path only) ─────────────────────────────────────────
# Paste this block into the existing login() function, replacing the
# "# ── HTML form path ──" section.

    # ── HTML form path ───────────────────────────────────────────────────────
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash("Invalid username or password.", "danger")
            return render_template("auth/login.html", form=form), 401

        login_user(user, remember=form.remember_me.data)
        flash(f"Welcome back, {user.username}! You are now logged in.", "success")

        # TODO: read the `next` query parameter
        next_url =  None # replace None with request.args.get("next")

        # TODO: redirect to next_url if it is safe, otherwise get_recipes
        #   if is_safe_url(next_url):
        #       return redirect(next_url)
        return redirect(url_for("main_bp.get_recipes"))

    return render_template("auth/login.html", form=form)

