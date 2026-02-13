import pytest
import jwt
from app.main import (
    create_token,
    verify_token,
    require_admin,
    SECRET_KEY,
    ALGORITHM
)
from fastapi import HTTPException


def test_create_token_valid():
    token = create_token("admin", "admin")
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert decoded["sub"] == "admin"
    assert decoded["role"] == "admin"
    assert "exp" in decoded


def test_create_token_invalid_signature():
    token = create_token("admin", "admin")

    with pytest.raises(jwt.InvalidTokenError):
        jwt.decode(token, "wrong_secret", algorithms=[ALGORITHM])


def test_verify_token_valid(monkeypatch):
    token = create_token("admin", "admin")

    class MockCredentials:
        credentials = token

    payload = verify_token(MockCredentials())
    assert payload["role"] == "admin"


def test_verify_token_invalid():
    class MockCredentials:
        credentials = "invalid.token.value"

    with pytest.raises(HTTPException):
        verify_token(MockCredentials())


def test_require_admin_success():
    payload = {"role": "admin"}
    result = require_admin(payload)
    assert result["role"] == "admin"


def test_require_admin_forbidden():
    payload = {"role": "user"}

    with pytest.raises(HTTPException) as exc:
        require_admin(payload)

    assert exc.value.status_code == 403


def test_profit_margin_calculation():
    price = 100
    cost = 50
    margin = (price - cost) / cost * 100

    assert margin == 100.0


def test_inventory_value_calculation_logic():
    products = [
        {"price": 10, "quantity": 2},
        {"price": 5, "quantity": 4},
    ]

    total = 0
    for p in products:
        total += p["price"] * p["quantity"]

    assert total == 40

#-------
def test_create_token():
    token = create_token("admin", "admin")
    decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    assert decoded["sub"] == "admin"


def test_verify_token_invalid():
    class MockCredentials:
        credentials = "invalid.token"

    with pytest.raises(HTTPException):
        verify_token(MockCredentials())


def test_verify_token_expired(monkeypatch):
    def fake_decode(*args, **kwargs):
        raise jwt.ExpiredSignatureError("Expired")

    monkeypatch.setattr(jwt, "decode", fake_decode)

    class MockCredentials:
        credentials = "expired.token"


    with pytest.raises(Exception):
        verify_token(MockCredentials())


def test_require_admin_success():
    payload = {"role": "admin"}
    assert require_admin(payload)["role"] == "admin"


def test_require_admin_fail():
    payload = {"role": "user"}

    with pytest.raises(HTTPException):
        require_admin(payload)