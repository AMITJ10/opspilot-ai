import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

from src.dashboard import (
    setup_page, apply_theme,
    load_filtered_data, page_header
)

setup_page("Revenue Forecasting")
apply_theme()
df = load_filtered_data()

page_header(
    "Predictive Revenue Analytics",
    "Historical monthly revenue and baseline projections"
)

monthly = (
    df.set_index("order_date")
    .resample("MS")["revenue"]
    .sum()
    .reset_index()
)

if len(monthly) < 4:
    st.warning("At least four months of data are required.")
    st.stop()

# Exclude an incomplete latest calendar month
last_date = df["order_date"].max()
month_end = last_date + pd.offsets.MonthEnd(0)

if last_date.date() < month_end.date():
    monthly = monthly.iloc[:-1].copy()

if len(monthly) < 4:
    st.warning("Insufficient complete monthly history.")
    st.stop()

monthly["index"] = np.arange(len(monthly))

model = LinearRegression()
model.fit(monthly[["index"]], monthly["revenue"])

months = st.slider("Forecast Horizon", 1, 12, 3)

future = pd.DataFrame({
    "index": np.arange(
        len(monthly),
        len(monthly) + months
    )
})

future["revenue"] = np.maximum(
    model.predict(future[["index"]]),
    0
)

future["month"] = pd.date_range(
    monthly["order_date"].max()
    + pd.offsets.MonthBegin(1),
    periods=months,
    freq="MS"
)

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=monthly["order_date"],
    y=monthly["revenue"],
    mode="lines+markers",
    name="Historical Revenue"
))

fig.add_trace(go.Scatter(
    x=future["month"],
    y=future["revenue"],
    mode="lines+markers",
    name="Forecast",
    line=dict(dash="dash", color="#38BDF8")
))

fig.update_layout(
    title="Revenue Forecast",
    template="plotly_dark",
    height=450,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Forecasted Monthly Revenue")
st.dataframe(
    future[["month", "revenue"]],
    use_container_width=True,
    hide_index=True
)

st.info(
    "This is a simple linear-trend baseline, not a validated "
    "business forecast. Evaluate it against held-out historical "
    "months before using predictions for decisions."
)
