import pytest
from app.models import User


def test_password_setter_hashes():
    """Setting password must store a hash, not plain text."""
    user = User(username="alice", email="alice@example.com")
    user.password = "s3cret!"
    assert user.password_hash is not None
    assert user.password_hash != "s3cret!"


def test_password_getter_raises():
    """Reading .password must raise AttributeError."""
    user = User(username="bob", email="bob@example.com")
    user.password = "s3cret!"
    with pytest.raises(AttributeError):
        _ = user.password


def test_verify_password_correct():
    """verify_password returns True for the correct password."""
    user = User(username="carol", email="carol@example.com")
    user.password = "mypassword"
    assert user.verify_password("mypassword") is True


def test_verify_password_wrong():
    """verify_password returns False for wrong password."""
    user = User(username="dave", email="dave@example.com")
    user.password = "mypassword"
    assert user.verify_password("wrongpassword") is False


def test_two_users_same_password_different_hashes():
    """Salting must produce different hashes for the same password."""
    u1 = User(username="eve",   email="eve@example.com")
    u2 = User(username="frank", email="frank@example.com")
    u1.password = u2.password = "samepass"
    assert u1.password_hash != u2.password_hash

