import streamlit as st
import plotly.express as px
from src.dashboard import (
    setup_page, apply_theme,
    load_filtered_data, money, page_header
)

setup_page("Financial Analytics")
apply_theme()
df = load_filtered_data()

page_header(
    "Financial Intelligence",
    "Revenue, direct costs and gross profitability"
)

revenue = df["revenue"].sum()
cost = df["cost"].sum()
profit = df["profit"].sum()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Revenue", money(revenue))
c2.metric("Direct Cost", money(cost))
c3.metric("Gross Profit", money(profit))
c4.metric(
    "Gross Margin",
    f"{profit / revenue * 100:.1f}%" if revenue else "0%"
)

finance = df.groupby(
    "site", as_index=False
)[["revenue", "cost", "profit"]].sum()

fig = px.bar(
    finance,
    x="site",
    y=["revenue", "cost", "profit"],
    barmode="group",
    title="Plant Financial Comparison",
    template="plotly_dark"
)

st.plotly_chart(fig, use_container_width=True)

finance["margin_pct"] = (
    finance["profit"] / finance["revenue"] * 100
).where(finance["revenue"] != 0, 0)

st.subheader("Plant Financial Summary")
st.dataframe(finance, use_container_width=True)

st.download_button(
    "Download Financial Report",
    finance.to_csv(index=False).encode("utf-8"),
    file_name="financial_report.csv",
    mime="text/csv"
)
