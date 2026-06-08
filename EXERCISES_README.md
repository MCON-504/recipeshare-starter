# In-Class Exercises — Flask Forms & Authentication

Work through these three exercises in order. Each one builds directly on the
code already in the project. Starter code is provided in `exercises/`.

> Note: all `main_bp` routes are mounted under `/api` in this project.

---

## Exercise 1 — Recipe Detail Page

**Goal:** Apply the same `request.is_json` dual-mode pattern to `get_recipe`
so that a browser request renders an HTML page for a single recipe.

### What to do

1. Create the template `app/templates/recipe_detail.html` by copying the starter file from `exercises/recipe_detail.html`.
2. Update `get_recipe` in `app/routes.py`:
   - If `request.is_json` → keep returning `jsonify(recipe.to_dict())` *(already there, don't break it)*
   - Otherwise → `return render_template("recipe_detail.html", recipe=recipe)`
3. In `app/templates/home.html`, wrap each recipe card title in a link to the detail page:
   ```html
   <a href="{{ url_for('main_bp.get_recipe', recipe_id=recipe.id) }}">
       {{ recipe.title }}
   </a>
   ```

### What you should see

- `GET /api/recipes` -> clicking a recipe card takes you to `/api/recipes/1`
- `/api/recipes/1` shows the full title, description, instructions, and prep time
- `GET /api/recipes/1` still returns JSON when the request includes
  `Content-Type: application/json` (so `request.is_json` is `True`)

### Files to edit
- `app/routes.py`
- `app/templates/home.html`
- `app/templates/recipe_detail.html` *(create from `exercises/recipe_detail.html`)*

---

## Exercise 2 — Redirect After Logout

**Goal:** Make the browser logout experience feel complete — flash a message
and send the user back to the recipe list. Keep the JSON response for API clients.

### What to do

Update the `logout` view in `app/auth/views.py`:

```python
@auth_bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    if request.is_json:
        return jsonify({"message": "logged out"}), 200
    flash("You have been logged out.", "info")
    return redirect(url_for("main_bp.get_recipes"))
```

### What you should see

- Clicking the Logout button in the navbar flashes "You have been logged out."
  and lands on the recipe list
- `POST /auth/logout` with `Content-Type: application/json` still returns
  `{"message": "logged out"}`

### Files to edit
- `app/auth/views.py`

---

## Exercise 3 — Auto-Login After Registration

**Goal:** After a successful registration, log the user in immediately and
redirect to the recipe list instead of asking them to log in again.

### What to do

In the HTML form path of `register` in `app/auth/views.py`, add a
`login_user()` call right after `db.session.commit()` and update the redirect:

```python
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
    login_user(user)                                      # ← add this
    flash(f"Welcome, {user.username}! Your account has been created.", "success")
    return redirect(url_for("main_bp.get_recipes"))       # ← change this
```

### What you should see

- Registering a new account lands directly on the recipe list, already logged in
- The navbar shows "Hi, \<username\>" immediately
- The JSON API path (`request.is_json`) is unchanged

### Files to edit
- `app/auth/views.py`

