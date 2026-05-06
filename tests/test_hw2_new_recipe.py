"""
Tests for Homework 2 — Create Recipe Form
==========================================
Covers every acceptance criterion listed in HOMEWORK_README.md.

Run with:
    pytest tests/test_hw2_new_recipe.py -v
"""
import pytest
from app import create_app
from app.extensions import db


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def client():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,   # disable CSRF so form POSTs work in tests
    })
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()


VALID_FORM = {
    "title": "Test Soup",
    "description": "A warm bowl of soup.",
    "instructions": "Boil water. Add ingredients. Serve.",
    "prep_time": 15,
}


def register_and_login(client, username="alice", email="alice@test.com", password="s3cret!!"):
    """Register and log in a user via the JSON API (always works)."""
    client.post("/auth/register", json={"username": username, "email": email, "password": password})
    client.post("/auth/login", json={"username": username, "password": password})


# ── Acceptance criterion 1 ────────────────────────────────────────────────────
# Unauthenticated GET /api/recipes/new  →  redirect to login

def test_new_recipe_get_requires_login(client):
    rv = client.get("/api/recipes/new")
    assert rv.status_code in (302, 401), (
        "Expected a redirect (302) or 401 for unauthenticated access"
    )
    # If it's a redirect it should point at the login page
    if rv.status_code == 302:
        assert "login" in rv.headers["Location"]


# ── Acceptance criterion 2 ────────────────────────────────────────────────────
# Authenticated GET /api/recipes/new  →  200 with the form

def test_new_recipe_get_renders_form(client):
    register_and_login(client)
    rv = client.get("/api/recipes/new")
    assert rv.status_code == 200
    body = rv.data.decode()
    assert "form" in body.lower(), "Response should contain an HTML <form>"


# ── Acceptance criterion 3 ────────────────────────────────────────────────────
# Valid form POST  →  recipe saved, redirect to detail page, flash "Recipe created!"

def test_new_recipe_valid_post_redirects(client):
    register_and_login(client)
    rv = client.post("/api/recipes/new", data=VALID_FORM, follow_redirects=False)
    assert rv.status_code == 302, "Valid submission should redirect"


def test_new_recipe_valid_post_saves_recipe(client):
    register_and_login(client)
    client.post("/api/recipes/new", data=VALID_FORM, follow_redirects=True)
    # Recipe should now appear in the recipe list
    recipes = client.get("/api/recipes", content_type="application/json").get_json()
    assert any(r["title"] == VALID_FORM["title"] for r in recipes), (
        "Recipe should be persisted in the database after a valid form submission"
    )


def test_new_recipe_valid_post_flashes_success(client):
    register_and_login(client)
    rv = client.post("/api/recipes/new", data=VALID_FORM, follow_redirects=True)
    assert b"Recipe created" in rv.data, (
        "Expected 'Recipe created!' flash message in the response HTML"
    )


def test_new_recipe_valid_post_redirects_to_detail(client):
    register_and_login(client)
    rv = client.post("/api/recipes/new", data=VALID_FORM, follow_redirects=False)
    # Location should be /api/recipes/<id>  (an integer at the end)
    location = rv.headers.get("Location", "")
    assert "/api/recipes/" in location, (
        f"Expected redirect to recipe detail page, got: {location}"
    )
    # The last path segment should be a number
    recipe_id = location.rstrip("/").rsplit("/", 1)[-1]
    assert recipe_id.isdigit(), f"Expected numeric recipe id in redirect URL, got: {recipe_id}"


# ── Acceptance criterion 4 ────────────────────────────────────────────────────
# Missing required field  →  form re-rendered with validation errors

@pytest.mark.parametrize("missing_field", ["title", "description", "instructions", "prep_time"])
def test_new_recipe_missing_field_shows_errors(client, missing_field):
    register_and_login(client)
    bad_data = {k: v for k, v in VALID_FORM.items() if k != missing_field}
    rv = client.post("/api/recipes/new", data=bad_data)
    assert rv.status_code == 200, (
        f"Should re-render the form (200) when '{missing_field}' is missing, not redirect"
    )
    body = rv.data.decode()
    # The form should still be present (not a redirect away)
    assert "form" in body.lower()


# ── Acceptance criterion 5 ────────────────────────────────────────────────────
# POST /api/recipes with JSON  →  unchanged (returns 201 JSON)

def test_create_recipe_json_still_works(client):
    register_and_login(client)
    rv = client.post("/api/recipes", json=VALID_FORM)
    assert rv.status_code == 201
    data = rv.get_json()
    assert data["title"] == VALID_FORM["title"]
    assert "id" in data


