import streamlit as st
import plotly.express as px

from src.dashboard import (
    setup_page,
    apply_theme,
    load_filtered_data,
    page_header
)

from src.ai.anomalies import detect_anomalies
from src.ai.insights import generate_insights
from src.ai.forecasting import (
    prepare_monthly_data,
    train_models,
    forecast_revenue
)

setup_page("AI Intelligence", "🧠")
apply_theme()

df = load_filtered_data()

page_header(
    "AI Business Intelligence",
    "Forecasts, anomaly detection and business insights"
)

tab1, tab2, tab3 = st.tabs([
    "Business Insights",
    "Anomaly Detection",
    "AI Forecasting"
])

with tab1:
    st.subheader("Automated Business Insights")

    insights = generate_insights(df)

    for i, insight in enumerate(insights, start=1):
        st.info(f"{i}. {insight}")

with tab2:
    st.subheader("Unusual Transactions")

    contamination = st.slider(
        "Expected Anomaly Percentage",
        min_value=1,
        max_value=15,
        value=5
    )

    try:
        results = detect_anomalies(
            df,
            contamination=contamination / 100
        )

        anomalies = results[
            results["anomaly"]
        ].copy()

        c1, c2 = st.columns(2)

        c1.metric(
            "Analyzed Transactions",
            len(results)
        )

        c2.metric(
            "Flagged Transactions",
            len(anomalies)
        )

        if not anomalies.empty:
            fig = px.scatter(
                results,
                x="quantity",
                y="revenue",
                color="anomaly",
                hover_data=[
                    "order_id", "customer", "site"
                ],
                title="Transaction Anomaly Detection",
                template="plotly_dark"
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.dataframe(
                anomalies[
                    [
                        "order_id",
                        "customer",
                        "site",
                        "revenue",
                        "profit",
                        "anomaly_score"
                    ]
                ],
                use_container_width=True
            )
        else:
            st.success("No anomalies detected.")

    except ValueError as exc:
        st.warning(str(exc))

with tab3:
    st.subheader("Machine Learning Revenue Forecast")

    monthly = prepare_monthly_data(df)

    if len(monthly) < 11:
        st.warning(
            "At least 11 complete months are required. "
            "Upload more historical data to enable "
            "model comparison and forecasting."
        )
    else:
        with st.spinner("Training forecasting models..."):
            model, model_name, scores = train_models(
                monthly
            )

        st.success(f"Selected Model: {model_name}")

        st.markdown("### Model Validation MAE")

        for name, score in scores.items():
            st.metric(name, f"INR {score:,.0f}")

        horizon = st.slider(
            "Forecast Months",
            min_value=1,
            max_value=12,
            value=3
        )

        forecast = forecast_revenue(
            monthly,
            model,
            months=horizon
        )

        historical = monthly.reset_index()
        historical.columns = ["month", "revenue"]

        fig = px.line(
            historical,
            x="month",
            y="revenue",
            title="Historical Revenue",
            template="plotly_dark"
        )

        fig.add_scatter(
            x=forecast["month"],
            y=forecast["predicted_revenue"],
            mode="lines+markers",
            name="AI Forecast",
            line=dict(
                color="#38BDF8",
                dash="dash"
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.dataframe(
            forecast,
            use_container_width=True,
            hide_index=True
        )

        st.caption(
            "Experimental forecast. Validation uses "
            "historical one-step predictions; "
            "multi-month forecast accuracy is not "
            "established by these MAE scores."
        )
