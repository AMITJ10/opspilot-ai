import streamlit as st
import plotly.express as px
from src.dashboard import (
    setup_page, apply_theme,
    load_filtered_data, money, page_header
)

setup_page("Sales Analytics")
apply_theme()
df = load_filtered_data()

page_header(
    "Sales Intelligence",
    "Customer, product and plant sales performance"
)

c1, c2, c3 = st.columns(3)
c1.metric("Total Sales", money(df["revenue"].sum()))
c2.metric("Active Customers", df["customer"].nunique())
c3.metric("Average Order Value", money(df["revenue"].mean()))

customers = df.groupby(
    "customer", as_index=False
).agg(
    revenue=("revenue", "sum"),
    orders=("order_id", "count"),
    profit=("profit", "sum")
).sort_values("revenue", ascending=False)

fig = px.bar(
    customers.head(15),
    x="revenue",
    y="customer",
    orientation="h",
    color="profit",
    title="Top Customers by Revenue",
    template="plotly_dark"
)

fig.update_layout(
    yaxis={"categoryorder": "total ascending"},
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)

with left:
    product = df.groupby(
        "product", as_index=False
    )["revenue"].sum()

    fig = px.pie(
        product, names="product", values="revenue",
        hole=0.5, title="Product Revenue Share",
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)

with right:
    site = df.groupby(
        "site", as_index=False
    )["revenue"].sum()

    fig = px.bar(
        site, x="site", y="revenue",
        color="site", title="Sales by Plant",
        template="plotly_dark"
    )
    st.plotly_chart(fig, use_container_width=True)

st.subheader("Customer Performance")
st.dataframe(customers, use_container_width=True)
