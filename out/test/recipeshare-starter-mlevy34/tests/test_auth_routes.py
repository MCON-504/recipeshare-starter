import pytest
from app import create_app
from app.extensions import db


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


def register(client, username="alice", email="alice@test.com", password="s3cret!!"):
    return client.post("/auth/register", json={
        "username": username, "email": email, "password": password
    })


# ── Registration ──────────────────────────────────────

def test_register_success(client):
    rv = register(client)
    assert rv.status_code == 201
    data = rv.get_json()
    assert data["username"] == "alice"
    assert "password_hash" not in data   # never leak the hash


def test_register_duplicate_username(client):
    register(client)
    rv = register(client, email="other@test.com")
    assert rv.status_code == 409


def test_register_duplicate_email(client):
    register(client)
    rv = register(client, username="other")
    assert rv.status_code == 409


def test_register_short_password(client):
    rv = register(client, password="short")
    assert rv.status_code == 400


def test_register_missing_fields(client):
    rv = client.post("/auth/register", json={"username": "alice"})
    assert rv.status_code == 400


# ── Login ─────────────────────────────────────────────

def test_login_success(client):
    register(client)
    rv = client.post("/auth/login", json={
        "username": "alice", "password": "s3cret!!"
    })
    assert rv.status_code == 200


def test_login_wrong_password(client):
    register(client)
    rv = client.post("/auth/login", json={
        "username": "alice", "password": "badpass"
    })
    assert rv.status_code == 401


def test_login_unknown_user(client):
    rv = client.post("/auth/login", json={
        "username": "nobody", "password": "whatever"
    })
    assert rv.status_code == 401


# ── Protected route ───────────────────────────────────

def test_protected_route_requires_login(client):
    rv = client.post("/api/recipes", json={"title": "X", "body": "Y"})
    assert rv.status_code in (401, 302)  # redirect or 401


# ── Logout ────────────────────────────────────────────

def test_logout_requires_login(client):
    rv = client.post("/auth/logout")
    assert rv.status_code in (401, 302)


def test_logout_success(client):
    register(client)
    client.post("/auth/login", json={"username": "alice", "password": "s3cret!!"})
    rv = client.post("/auth/logout")
    assert rv.status_code == 200
    assert rv.get_json()["message"] == "logged out"

