# Homework — Flask Forms & Authentication

These two features extend the in-class work. Both involve patterns you have
already seen — form classes, dual-mode routes, `@login_required`, and
`current_user` — applied to new problems.

> Note: all `main_bp` routes are mounted under `/api` in this project.

Submit a link to your GitHub branch before the next class.

---

## Assignment 1 — `next` Parameter After Login

### Background

When an unauthenticated user tries to visit a protected route (e.g. a future
"create recipe" page), Flask-Login redirects them to the login page and
appends `?next=/api/recipes/new` to the URL. After a successful login the user
should land on the page they originally wanted, not always the recipe list.

### Requirements

1. After a successful **form** login, read `request.args.get("next")`.
2. If a `next` value exists **and** is a safe relative URL, redirect there.
3. Otherwise fall back to `url_for("main_bp.get_recipes")`.
4. The JSON login path (when `request.is_json` is `True`) must remain unchanged.
5. Pass the `next` parameter through the login form's `action` URL so it
   survives the POST:
   ```html
   <form method="POST" action="{{ url_for('auth.login', next=request.args.get('next')) }}">
   ```
   Without this, `?next=...` is only on the GET request (the redirect from
   Flask-Login) and is lost when the form submits.

### Safety rule

Only redirect to `next` if it is a relative path (starts with `/` and does
**not** start with `//`). This prevents an open-redirect attack where an
attacker tricks a user into being sent to a malicious external site.

```python
from urllib.parse import urlparse

def is_safe_url(target: str) -> bool:
    parsed = urlparse(target)
    return not parsed.netloc and parsed.path.startswith("/")
```

### Acceptance criteria

| Scenario | Expected behaviour |
|---|---|
| Visit `/api/recipes` (no `next`) → login | Redirect to `/api/recipes` |
| Visit a protected URL → redirected to `/auth/login?next=/api/recipes/new` → login | Redirect to `/api/recipes/new` |
| `?next=https://evil.com` | Ignored — redirect to `/api/recipes` |
| JSON `POST /auth/login` | Unchanged — returns `user.to_dict()` |

### Files to edit
- `app/auth/views.py`
- `app/templates/auth/login.html`

### Starter file
`exercises/hw1_views_login_starter.py` — contains the `is_safe_url` helper
stub and the updated HTML form path with `TODO` comments showing exactly where
to make your changes. Copy the relevant pieces into `app/auth/views.py`.

---

## Assignment 2 — Create Recipe Form

### Background

The `POST /api/recipes` endpoint already creates recipes for API clients. Add a
browser form at `GET /api/recipes/new` so a logged-in user can submit a new
recipe through the web UI.

### Requirements

1. **Form class** — create `RecipeForm` in `app/routes.py` (or a new
   `app/forms.py`) with these fields:

   | Field | Type | Validators |
   |---|---|---|
   | `title` | `StringField` | `DataRequired()`, `Length(max=150)` |
   | `description` | `TextAreaField` | `DataRequired()` |
   | `instructions` | `TextAreaField` | `DataRequired()` |
   | `prep_time` | `IntegerField` | `DataRequired()`, `NumberRange(min=1)` |
   | `submit` | `SubmitField` | — |

2. **Route** — add `GET /api/recipes/new` and `POST /api/recipes/new`:
   - `GET` → render the blank form (login required)
   - `POST` → validate, create the `Recipe`, commit, flash success, redirect
     to the new recipe's detail page

3. **Template** — create `app/templates/recipe_form.html` that renders the
   form fields, CSRF token, and validation errors.

4. **Link** — in `home.html`, show a "＋ Add Recipe" link for authenticated
   users only:
   ```html
   {% if current_user.is_authenticated %}
   <a href="{{ url_for('main_bp.new_recipe') }}" class="btn btn-primary">
       ＋ Add Recipe
   </a>
   {% endif %}
   ```

### Acceptance criteria

| Scenario | Expected behaviour |
|---|---|
| Unauthenticated `GET /api/recipes/new` | Redirect to login |
| Valid form submission | Recipe saved, redirect to detail page, flash "Recipe created!" |
| Missing required field | Form re-rendered with validation errors shown |
| `POST /api/recipes` with JSON (`request.is_json` is `True`) | Unchanged — returns 201 JSON |

### Files to create / edit
- `app/routes.py` — add `RecipeForm` and two new route functions
- `app/templates/recipe_form.html` — new file
- `app/templates/home.html` — add the "＋ Add Recipe" link

### Starter files
| File | Use for |
|---|---|
| `exercises/hw2_routes_new_recipe_starter.py` | `RecipeForm` class and `new_recipe()` route skeleton with `TODO` comments — copy into `app/routes.py` |
| `exercises/hw2_recipe_form.html` | Template skeleton with field-rendering pattern commented in — copy to `app/templates/recipe_form.html` and fill in the `TODO` sections |

