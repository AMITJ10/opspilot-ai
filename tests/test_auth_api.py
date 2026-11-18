from fastapi.testclient import TestClient

from backend.main import app
from backend.api.auth import get_current_user, UserResponse
from backend.core.jwt_security import create_access_token

client = TestClient(app)


def test_login_success(monkeypatch):
    def fake_authenticate(email, password):
        if email == "test@example.com" and password == "valid-password":
            return {
                "id": 1,
                "email": email,
                "company_id": 5,
                "role": "owner",
            }
        return None

    monkeypatch.setattr(
        "backend.api.auth.authenticate_user",
        fake_authenticate,
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "valid-password",
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["token_type"] == "bearer"
    assert data["access_token"]


def test_login_invalid_credentials(monkeypatch):
    monkeypatch.setattr(
        "backend.api.auth.authenticate_user",
        lambda email, password: None,
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "wrong-password",
        },
    )

    assert response.status_code == 401


def test_me_without_token():
    response = client.get("/auth/me")
    assert response.status_code == 401


def test_me_invalid_token():
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid-token"},
    )
    assert response.status_code == 401


def test_me_valid_user():
    def fake_current_user():
        return UserResponse(
            id=1,
            email="test@example.com",
            company_id=5,
            company_name="Test Company",
            role="owner",
            is_active=True,
        )

    app.dependency_overrides[get_current_user] = fake_current_user

    try:
        response = client.get("/auth/me")

        assert response.status_code == 200
        assert response.json()["company_id"] == 5
        assert response.json()["role"] == "owner"

    finally:
        app.dependency_overrides.clear()


def test_check_valid_user():
    def fake_current_user():
        return UserResponse(
            id=1,
            email="test@example.com",
            company_id=5,
            company_name="Test Company",
            role="owner",
            is_active=True,
        )

    app.dependency_overrides[get_current_user] = fake_current_user

    try:
        response = client.get("/auth/check")

        assert response.status_code == 200
        assert response.json()["authenticated"] is True

    finally:
        app.dependency_overrides.clear()


def test_me_with_unknown_user():
    token = create_access_token(999999)

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401
