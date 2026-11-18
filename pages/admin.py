import streamlit as st
import pandas as pd

from src.dashboard import setup_page, apply_theme
from src.security.access import require_role
from src.security.admin import (
    list_company_users,
    create_company_user,
    set_user_active
)

setup_page("Company Administration", "🔐")
apply_theme()

user = require_role("owner", "admin")

st.title("Company Administration")
st.caption(f"Workspace: {user['company_name']}")

tab1, tab2 = st.tabs([
    "Team Members",
    "Create User"
])

with tab1:
    users = list_company_users(user["company_id"])

    st.metric("Total Users", len(users))

    st.dataframe(
        pd.DataFrame(users),
        use_container_width=True,
        hide_index=True
    )

    manageable = [
        item for item in users
        if item["role"] != "owner"
    ]

    if manageable:
        selected_id = st.selectbox(
            "Select User",
            options=[u["id"] for u in manageable],
            format_func=lambda uid: next(
                u["email"] for u in manageable
                if u["id"] == uid
            )
        )

        selected = next(
            u for u in manageable
            if u["id"] == selected_id
        )

        action = (
            "Deactivate User"
            if selected["active"]
            else "Reactivate User"
        )

        if st.button(action):
            set_user_active(
                user["company_id"],
                selected_id,
                not selected["active"]
            )
            st.success("User status updated")
            st.rerun()

with tab2:
    with st.form("create_user"):
        email = st.text_input("Email Address")

        password = st.text_input(
            "Temporary Password",
            type="password"
        )

        role = st.selectbox(
            "User Role",
            ["viewer", "admin"]
        )

        submitted = st.form_submit_button(
            "Create User"
        )

    if submitted:
        try:
            create_company_user(
                company_id=user["company_id"],
                email=email,
                password=password,
                role=role
            )
            st.success("User created successfully")

        except ValueError as exc:
            st.error(str(exc))
