import pandas as pd


def generate_insights(df):
    insights = []

    if df.empty:
        return ["No business data available."]

    revenue = df["revenue"].sum()
    profit = df["profit"].sum()

    margin = (
        profit / revenue * 100
        if revenue > 0 else 0
    )

    if margin < 15:
        insights.append(
            f"Gross margin is {margin:.1f}%. "
            "Review direct costs and pricing."
        )
    else:
        insights.append(
            f"Gross margin is {margin:.1f}%."
        )

    customer_sales = (
        df.groupby("customer")["revenue"]
        .sum()
        .sort_values(ascending=False)
    )

    if not customer_sales.empty and revenue > 0:
        top_customer = customer_sales.index[0]
        share = customer_sales.iloc[0] / revenue * 100

        insights.append(
            f"{top_customer} contributes "
            f"{share:.1f}% of total revenue."
        )

        if share > 40:
            insights.append(
                "Revenue is concentrated in one customer. "
                "Consider diversifying the customer base."
            )

    plant_profit = (
        df.groupby("site")["profit"]
        .sum()
        .sort_values()
    )

    if not plant_profit.empty:
        weakest = plant_profit.index[0]

        insights.append(
            f"{weakest} has the lowest total gross profit "
            "among the selected plants."
        )

    monthly = (
        df.set_index("order_date")
        .resample("MS")["revenue"]
        .sum()
    )

    if len(monthly) >= 2:
        previous = monthly.iloc[-2]
        current = monthly.iloc[-1]

        if previous > 0:
            growth = (current / previous - 1) * 100

            insights.append(
                f"Revenue changed by {growth:+.1f}% "
                "between the last two represented months."
            )

    return insights
