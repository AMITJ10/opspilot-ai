from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.core.jwt_security import (
    create_access_token,
    verify_access_token,
)
from src.database.connection import SessionLocal
from src.security.auth import authenticate_user
from src.security.models import Company, User


router = APIRouter(prefix="/auth", tags=["Authentication"])

bearer_scheme = HTTPBearer(auto_error=False)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 1800


class UserResponse(BaseModel):
    id: int
    email: str
    company_id: int
    company_name: str
    role: str
    is_active: bool


def get_db():
    with SessionLocal() as session:
        yield session


def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None,
        Depends(bearer_scheme),
    ],
    session: Annotated[Session, Depends(get_db)],
) -> UserResponse:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id = verify_access_token(credentials.credentials)

    result = session.execute(
        select(User, Company.name)
        .join(Company, User.company_id == Company.id)
        .where(User.id == user_id, User.is_active.is_(True))
    ).first()

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User account unavailable",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user, company_name = result

    return UserResponse(
        id=user.id,
        email=user.email,
        company_id=user.company_id,
        company_name=company_name,
        role=user.role,
        is_active=user.is_active,
    )


@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest):
    user = authenticate_user(data.email, data.password)

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return TokenResponse(
        access_token=create_access_token(user["id"])
    )


@router.get("/me", response_model=UserResponse)
def me(
    user: Annotated[UserResponse, Depends(get_current_user)]
):
    return user


@router.get("/check")
def check_auth(
    user: Annotated[UserResponse, Depends(get_current_user)]
):
    return {
        "authenticated": True,
        "user_id": user.id,
        "company_id": user.company_id,
    }
