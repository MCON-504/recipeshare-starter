import pytest
from app import create_app
from app.extensions import db


# ── Fixtures ──────────────────────────────────────────

@pytest.fixture
def client():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
    })

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()


RECIPE = {
    "title": "Pasta Carbonara",
    "description": "Classic Roman pasta dish.",
    "instructions": "Boil pasta. Mix eggs and cheese. Combine.",
    "prep_time": 20,
}


def register_and_login(client, username="alice", email="alice@test.com", password="s3cret!!"):
    """Helper: register a user and log them in, returning the logged-in client."""
    client.post("/auth/register", json={
        "username": username, "email": email, "password": password
    })
    client.post("/auth/login", json={"username": username, "password": password})


# ── GET / ─────────────────────────────────────────────

def test_home(client):
    rv = client.get("/api/")
    assert rv.status_code == 200
    assert rv.get_json()["message"] == "RecipeShare API is running"


# ── GET /api/recipes ──────────────────────────────────

def test_get_recipes_empty(client):
    rv = client.get("/api/recipes")
    assert rv.status_code == 200
    assert rv.get_json() == []


def test_get_recipes_returns_list(client):
    register_and_login(client)
    client.post("/api/recipes", json=RECIPE)
    rv = client.get("/api/recipes")
    assert rv.status_code == 200
    data = rv.get_json()
    assert len(data) == 1
    assert data[0]["title"] == RECIPE["title"]


def test_get_recipes_returns_all_fields(client):
    register_and_login(client)
    client.post("/api/recipes", json=RECIPE)
    data = client.get("/api/recipes").get_json()
    recipe = data[0]
    for field in ("id", "title", "description", "instructions", "prep_time", "created_at", "user_id"):
        assert field in recipe


def test_get_recipes_ordered_newest_first(client):
    register_and_login(client)
    client.post("/api/recipes", json={**RECIPE, "title": "First"})
    client.post("/api/recipes", json={**RECIPE, "title": "Second"})
    data = client.get("/api/recipes").get_json()
    assert data[0]["title"] == "Second"
    assert data[1]["title"] == "First"


# ── GET /api/recipes/<id> ─────────────────────────────

def test_get_recipe_by_id(client):
    register_and_login(client)
    created = client.post("/api/recipes", json=RECIPE).get_json()
    rv = client.get(f"/api/recipes/{created['id']}")
    assert rv.status_code == 200
    assert rv.get_json()["title"] == RECIPE["title"]


def test_get_recipe_not_found(client):
    rv = client.get("/api/recipes/9999")
    assert rv.status_code == 404


# ── POST /api/recipes ─────────────────────────────────

def test_create_recipe_success(client):
    register_and_login(client)
    rv = client.post("/api/recipes", json=RECIPE)
    assert rv.status_code == 201
    data = rv.get_json()
    assert data["title"] == RECIPE["title"]
    assert data["prep_time"] == RECIPE["prep_time"]
    assert "id" in data


def test_create_recipe_requires_login(client):
    rv = client.post("/api/recipes", json=RECIPE)
    assert rv.status_code in (401, 302)


def test_create_recipe_missing_title(client):
    register_and_login(client)
    rv = client.post("/api/recipes", json={
        "description": "desc", "instructions": "inst", "prep_time": 10
    })
    assert rv.status_code == 400
    assert "title" in rv.get_json()["error"]


def test_create_recipe_missing_description(client):
    register_and_login(client)
    rv = client.post("/api/recipes", json={
        "title": "X", "instructions": "inst", "prep_time": 10
    })
    assert rv.status_code == 400
    assert "description" in rv.get_json()["error"]


def test_create_recipe_missing_instructions(client):
    register_and_login(client)
    rv = client.post("/api/recipes", json={
        "title": "X", "description": "desc", "prep_time": 10
    })
    assert rv.status_code == 400
    assert "instructions" in rv.get_json()["error"]


def test_create_recipe_missing_prep_time(client):
    register_and_login(client)
    rv = client.post("/api/recipes", json={
        "title": "X", "description": "desc", "instructions": "inst"
    })
    assert rv.status_code == 400
    assert "prep_time" in rv.get_json()["error"]


def test_create_recipe_missing_all_fields(client):
    register_and_login(client)
    rv = client.post("/api/recipes", json={})
    assert rv.status_code == 400


# ── DELETE /api/recipes/<id> ──────────────────────────

def test_delete_recipe_success(client):
    register_and_login(client)
    created = client.post("/api/recipes", json=RECIPE).get_json()
    rv = client.delete(f"/api/recipes/{created['id']}")
    assert rv.status_code == 204
    # Confirm it's gone
    assert client.get(f"/api/recipes/{created['id']}").status_code == 404


def test_delete_recipe_requires_login(client):
    register_and_login(client)
    created = client.post("/api/recipes", json=RECIPE).get_json()
    client.post("/auth/logout")
    rv = client.delete(f"/api/recipes/{created['id']}")
    assert rv.status_code in (401, 302)


def test_delete_recipe_not_found(client):
    register_and_login(client)
    rv = client.delete("/api/recipes/9999")
    assert rv.status_code == 404


def test_delete_recipe_forbidden_for_other_user(client):
    # alice creates a recipe
    register_and_login(client, username="alice", email="alice@test.com")
    created = client.post("/api/recipes", json=RECIPE).get_json()
    client.post("/auth/logout")

    # bob tries to delete it
    register_and_login(client, username="bob", email="bob@test.com")
    rv = client.delete(f"/api/recipes/{created['id']}")
    assert rv.status_code == 403

