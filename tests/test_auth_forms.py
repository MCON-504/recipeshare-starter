import pytest

from app import create_app, db
from app.models import User


@pytest.fixture
def client():
    app = create_app({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SECRET_KEY": "test-secret",
    })

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()


def register(client, username="alice", email="alice@example.com", password="password123"):
    return client.post("/auth/register", data={
        "username": username,
        "email": email,
        "password": password,
        "confirm_password": password,
    }, follow_redirects=True)


def login(client, username="alice", password="password123"):
    return client.post("/auth/login", data={
        "username": username,
        "password": password,
    }, follow_redirects=True)


def test_register_creates_user_with_hashed_password(client):
    response = register(client)
    assert response.status_code == 200

    user = User.query.filter_by(username="alice").first()
    assert user is not None
    assert user.password_hash != "password123"
    assert user.verify_password("password123") is True


def test_register_rejects_duplicate_username(client):
    register(client)
    response = register(client, email="other@example.com")
    assert b"already taken" in response.data


def test_login_success(client):
    register(client)
    response = login(client)
    assert b"logged in" in response.data.lower()


def test_login_wrong_password(client):
    register(client)
    response = login(client, password="wrong-password")
    assert response.status_code == 401
    assert b"invalid username or password" in response.data.lower()