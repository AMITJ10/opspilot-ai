from sqlalchemy import select
from src.database.connection import SessionLocal
from src.security.models import User
from src.security.auth import hash_password

ALLOWED_ROLES = {"admin", "viewer"}


def list_company_users(company_id):
    with SessionLocal() as session:
        users = session.scalars(
            select(User)
            .where(User.company_id == company_id)
            .order_by(User.id)
        ).all()

        return [
            {
                "id": user.id,
                "email": user.email,
                "role": user.role,
                "active": user.is_active
            }
            for user in users
        ]


def create_company_user(
    company_id,
    email,
    password,
    role="viewer"
):
    email = email.strip().lower()

    if role not in ALLOWED_ROLES:
        raise ValueError("Invalid role")

    if len(password) < 12:
        raise ValueError(
            "Password must contain at least 12 characters"
        )

    with SessionLocal.begin() as session:
        existing = session.scalar(
            select(User).where(User.email == email)
        )

        if existing:
            raise ValueError("Email already registered")

        user = User(
            company_id=company_id,
            email=email,
            password_hash=hash_password(password),
            role=role,
            is_active=True
        )

        session.add(user)


def set_user_active(company_id, user_id, active):
    with SessionLocal.begin() as session:
        user = session.scalar(
            select(User).where(
                User.id == user_id,
                User.company_id == company_id
            )
        )

        if not user:
            raise ValueError("User not found")

        if user.role == "owner":
            raise ValueError("Owner cannot be deactivated")

        user.is_active = active
