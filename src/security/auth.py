from pwdlib import PasswordHash
from sqlalchemy import select
from src.database.connection import SessionLocal
from src.security.models import Company, User

password_hasher = PasswordHash.recommended()


def hash_password(password):
    return password_hasher.hash(password)


def verify_password(password, password_hash):
    return password_hasher.verify(password, password_hash)


def register_company(company_name, email, password):
    company_name = company_name.strip()
    email = email.strip().lower()

    if not company_name:
        raise ValueError("Company name is required")

    if len(password) < 12:
        raise ValueError("Password must contain at least 12 characters")

    with SessionLocal.begin() as session:
        existing = session.scalar(
            select(User).where(User.email == email)
        )

        if existing:
            raise ValueError("Email is already registered")

        company = Company(name=company_name)
        session.add(company)
        session.flush()

        user = User(
            company_id=company.id,
            email=email,
            password_hash=hash_password(password),
            role="owner"
        )

        session.add(user)

        session.flush()

        return {
            "id": user.id,
            "email": user.email,
            "company_id": company.id,
            "company_name": company.name,
            "role": user.role
        }


def authenticate_user(email, password):
    email = email.strip().lower()

    with SessionLocal() as session:
        user = session.scalar(
            select(User).where(User.email == email)
        )

        if not user or not user.is_active:
            return None

        if not verify_password(password, user.password_hash):
            return None

        company = session.get(Company, user.company_id)

        return {
            "id": user.id,
            "email": user.email,
            "company_id": user.company_id,
            "company_name": company.name,
            "role": user.role
        }
