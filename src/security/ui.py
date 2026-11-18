import streamlit as st
from src.security.auth import (
    register_company,
    authenticate_user
)


def login_required():
    if "user" in st.session_state:
        return st.session_state["user"]

    st.title("OpsPilot AI")
    st.caption("Secure Business Analytics Platform")

    login_tab, register_tab = st.tabs(
        ["Sign In", "Create Company Account"]
    )

    with login_tab:
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input(
                "Password", type="password"
            )

            submitted = st.form_submit_button(
                "Sign In", use_container_width=True
            )

        if submitted:
            try:
                user = authenticate_user(email, password)

                if user:
                    st.session_state["user"] = user
                    st.rerun()
                else:
                    st.error("Invalid email or password")
            except Exception:
                st.error("Unable to sign in")

    with register_tab:
        with st.form("registration_form"):
            company = st.text_input("Company Name")
            email = st.text_input("Business Email")
            password = st.text_input(
                "Create Password",
                type="password"
            )

            submitted = st.form_submit_button(
                "Create Account",
                use_container_width=True
            )

        if submitted:
            try:
                user = register_company(
                    company, email, password
                )

                st.session_state["user"] = user
                st.rerun()

            except ValueError as exc:
                st.error(str(exc))

    st.stop()


def logout_button():
    if st.sidebar.button("Sign Out"):
        st.session_state.clear()
        st.rerun()
