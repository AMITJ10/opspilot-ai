import streamlit as st
import pandas as pd
from src.security.ui import logout_button
from src.database.repository import get_orders
from src.security.access import current_user

def money(value):
    return f"INR {value:,.0f}"

def setup_page(title, icon="📊"):
    st.set_page_config(
        page_title=f"{title} | OpsPilot AI",
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="expanded"
    )

def apply_theme():
    st.markdown("""
    <style>
    .stApp {
        background: #0b1220;
        color: #e5e7eb;
    }

    [data-testid="stSidebar"] {
        background: #111c2e;
        border-right: 1px solid #26344b;
    }

    [data-testid="stMetric"] {
        background: #17243a;
        border: 1px solid #2b3d57;
        padding: 20px;
        border-radius: 14px;
    }

    [data-testid="stMetricLabel"] {
        color: #94a3b8;
    }

    [data-testid="stMetricValue"] {
        color: #f8fafc;
    }

    h1, h2, h3 {
        letter-spacing: -0.5px;
    }

    div[data-testid="stPlotlyChart"] {
        background: #111c2e;
        border: 1px solid #26344b;
        border-radius: 14px;
        padding: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

def load_filtered_data():
    st.sidebar.markdown("## OpsPilot AI")
    st.sidebar.caption("Business Intelligence Platform")
    st.sidebar.divider()

    if st.sidebar.button("Refresh Database Data"):
        st.cache_data.clear()
        st.rerun()

    user = current_user()

    @st.cache_data(ttl=60)
    def fetch_data(company_id):
        return get_orders(tenant_id=company_id)

    try:
        df = fetch_data(user["company_id"])
    except Exception as exc:
        st.error(f"Database connection failed: {exc}")
        st.stop()

    if df.empty:
        st.warning("No orders found. Run the import script.")
        st.stop()

    st.sidebar.subheader("Global Filters")

    min_date = df["order_date"].min().date()
    max_date = df["order_date"].max().date()

    if "date_range" not in st.session_state:
        st.session_state["date_range"] = (
            min_date, max_date
        )

    selected_dates = st.sidebar.date_input(
        "Date Range",
        min_value=min_date,
        max_value=max_date,
        key="date_range"
    )

    sites = sorted(df["site"].dropna().unique().tolist())
    customers = sorted(
        df["customer"].dropna().unique().tolist()
    )
    products = sorted(
        df["product"].dropna().unique().tolist()
    )

    selected_sites = st.sidebar.multiselect(
        "Plants", sites,
        default=sites,
        key="selected_sites"
    )

    selected_customers = st.sidebar.multiselect(
        "Customers", customers,
        default=customers,
        key="selected_customers"
    )

    selected_products = st.sidebar.multiselect(
        "Products", products,
        default=products,
        key="selected_products"
    )

    if len(selected_dates) == 2:
        start, end = selected_dates
        df = df[
            df["order_date"].dt.date.between(start, end)
        ]

    df = df[
        df["site"].isin(selected_sites)
        & df["customer"].isin(selected_customers)
        & df["product"].isin(selected_products)
    ].copy()

    if df.empty:
        st.warning("No records match the selected filters.")
        st.stop()

    st.sidebar.divider()
    st.sidebar.caption(f"{len(df):,} matching transactions")

    return df

def page_header(title, description):
    st.title(title)
    st.caption(description)
    st.divider()


def account_sidebar():
    user = current_user()

    st.sidebar.divider()

    st.sidebar.markdown("### Workspace")

    st.sidebar.write(
        f"**Company:** {user['company_name']}"
    )

    st.sidebar.write(
        f"**User:** {user['email']}"
    )

    st.sidebar.write(
        f"**Role:** {user['role'].title()}"
    )

    logout_button()
