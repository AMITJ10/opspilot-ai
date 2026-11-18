import pytest
from fastapi import HTTPException

from backend.core.jwt_security import (
    create_access_token,
    verify_access_token,
)


def test_valid_access_token():
    token = create_access_token(1)
    assert verify_access_token(token) == 1


def test_invalid_access_token():
    with pytest.raises(HTTPException) as exc:
        verify_access_token("invalid.token.value")

    assert exc.value.status_code == 401


def test_invalid_user_id():
    token = create_access_token(0)

    with pytest.raises(HTTPException):
        verify_access_token(token)
