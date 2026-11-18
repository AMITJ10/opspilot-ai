import streamlit as st
import pandas as pd
import plotly.express as px

from src.dashboard import (
    setup_page, apply_theme,
    load_filtered_data, money, page_header
)

setup_page("Executive Overview")
apply_theme()


from src.security.access import current_user
from src.security.ui import logout_button

user = current_user()

st.sidebar.success(
    f"Company: {user['company_name']}"
)

st.sidebar.caption(
    f"Signed in as: {user['email']}"
)

st.sidebar.caption(
    f"Role: {user['role'].title()}"
)

logout_button()


df = load_filtered_data()

page_header(
    "Executive Command Center",
    "Live business performance from PostgreSQL"
)

revenue = df["revenue"].sum()
cost = df["cost"].sum()
profit = df["profit"].sum()
margin = (profit / revenue * 100) if revenue else 0

monthly = (
    df.assign(month=df["order_date"].dt.to_period("M"))
    .groupby("month", as_index=False)
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum")
    )
)

monthly["month"] = monthly["month"].dt.to_timestamp()

growth = None

if len(monthly) >= 2 and monthly["revenue"].iloc[-2] != 0:
    growth = (
        (monthly["revenue"].iloc[-1]
         / monthly["revenue"].iloc[-2]) - 1
    ) * 100

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Total Revenue",
    money(revenue),
    f"{growth:+.1f}%" if growth is not None else None
)
c2.metric("Gross Profit", money(profit))
c3.metric("Gross Margin", f"{margin:.1f}%")
c4.metric("Total Orders", f"{len(df):,}")

st.markdown("### Revenue and Profit Trends")

fig = px.line(
    monthly,
    x="month",
    y=["revenue", "profit"],
    markers=True,
    labels={
        "month": "Month",
        "value": "Amount (INR)",
        "variable": "Metric"
    }
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    hovermode="x unified",
    legend_title_text="",
    height=380
)

st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)

with left:
    st.markdown("### Revenue by Plant")

    plant = df.groupby(
        "site", as_index=False
    )["revenue"].sum()

    fig = px.bar(
        plant,
        x="site",
        y="revenue",
        color="site",
        text_auto=".2s",
        template="plotly_dark"
    )

    fig.update_layout(
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, use_container_width=True)

with right:
    st.markdown("### Revenue by Product")

    product = df.groupby(
        "product", as_index=False
    )["revenue"].sum()

    fig = px.pie(
        product,
        names="product",
        values="revenue",
        hole=0.65,
        template="plotly_dark"
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("### Top Customers")

customers = (
    df.groupby("customer", as_index=False)
    .agg(
        revenue=("revenue", "sum"),
        profit=("profit", "sum"),
        orders=("order_id", "count")
    )
    .sort_values("revenue", ascending=False)
    .head(10)
)

st.dataframe(
    customers,
    use_container_width=True,
    hide_index=True
)

st.download_button(
    "Export Filtered Transactions",
    df.to_csv(index=False).encode("utf-8"),
    file_name="opspilot_transactions.csv",
    mime="text/csv"
)
