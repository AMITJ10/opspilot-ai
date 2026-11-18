import streamlit as st
import plotly.express as px
from src.dashboard import (
    setup_page, apply_theme,
    load_filtered_data, page_header
)

setup_page("Operations Analytics")
apply_theme()
df = load_filtered_data()

page_header(
    "Operations Intelligence",
    "Plant output, product volume and operating efficiency"
)

c1, c2, c3 = st.columns(3)
c1.metric("Total Quantity", f"{df['quantity'].sum():,.0f}")
c2.metric("Active Plants", df["site"].nunique())
c3.metric("Average Order Quantity", f"{df['quantity'].mean():,.1f}")

plant = df.groupby(
    "site", as_index=False
).agg(
    quantity=("quantity", "sum"),
    orders=("order_id", "count"),
    revenue=("revenue", "sum")
)

fig = px.bar(
    plant,
    x="site",
    y="quantity",
    color="site",
    text_auto=True,
    title="Quantity by Plant",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

product = df.groupby(
    ["site", "product"], as_index=False
)["quantity"].sum()

fig = px.bar(
    product,
    x="site",
    y="quantity",
    color="product",
    barmode="stack",
    title="Product Volume by Plant",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Plant Performance")
st.dataframe(plant, use_container_width=True)
