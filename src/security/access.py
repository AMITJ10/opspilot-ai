import streamlit as st
from sqlalchemy import select

from src.database.connection import SessionLocal
from src.security.models import User, Company
from src.security.ui import login_required


def current_user():
    user_data = login_required()

    with SessionLocal() as session:
        user = session.scalar(
            select(User).where(
                User.id == user_data["id"],
                User.company_id == user_data["company_id"],
                User.is_active.is_(True)
            )
        )

        if user is None:
            st.session_state.pop("user", None)
            st.error("Session is no longer valid.")
            st.stop()

        company = session.get(Company, user.company_id)

        if company is None:
            st.error("Company account not found.")
            st.stop()

        return {
            "id": user.id,
            "email": user.email,
            "company_id": user.company_id,
            "company_name": company.name,
            "role": user.role
        }


def require_role(*roles):
    user = current_user()

    if user["role"] not in roles:
        st.error("You do not have permission to access this page.")
        st.stop()

    return user
