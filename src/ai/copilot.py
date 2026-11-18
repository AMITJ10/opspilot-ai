import re
import pandas as pd


def money(value):
    return f"INR {value:,.2f}"


def answer_question(df, question):
    if df.empty:
        return "No business data is available."

    q = question.lower().strip()

    if not q:
        return "Please enter a business question."

    revenue = df["revenue"].sum()
    profit = df["profit"].sum()
    cost = df["cost"].sum()

    if "margin" in q:
        margin = profit / revenue * 100 if revenue else 0
        return f"Your gross profit margin is {margin:.2f}%."

    if "total revenue" in q or "total sales" in q:
        return f"Total revenue is {money(revenue)}."

    if "total profit" in q or "gross profit" in q:
        return f"Total gross profit is {money(profit)}."

    if "total cost" in q:
        return f"Total direct cost is {money(cost)}."

    if "top" in q and "customer" in q:
        match = re.search(r"\btop\s+(\d+)", q)
        n = min(int(match.group(1)), 20) if match else 5

        result = (
            df.groupby("customer")["revenue"]
            .sum()
            .sort_values(ascending=False)
            .head(n)
        )

        lines = [
            f"{i}. {name}: {money(value)}"
            for i, (name, value) in enumerate(
                result.items(), start=1
            )
        ]

        return "Top customers by revenue:\n\n" + "\n\n".join(lines)

    if "plant" in q or "site" in q:
        if "profit" in q:
            metric = "profit"
        elif "quantity" in q or "production" in q:
            metric = "quantity"
        else:
            metric = "revenue"

        result = (
            df.groupby("site")[metric]
            .sum()
            .sort_values(ascending=False)
        )

        if result.empty:
            return "No plant data available."

        plant = result.index[0]
        value = result.iloc[0]

        formatted = (
            f"{value:,.0f}"
            if metric == "quantity"
            else money(value)
        )

        return (
            f"{plant} has the highest {metric}: "
            f"{formatted}."
        )

    if "order" in q and (
        "how many" in q or "total" in q
    ):
        return f"There are {len(df):,} orders."

    return (
        "I can answer questions about total revenue, "
        "gross profit, costs, margins, top customers, "
        "plant performance, and order counts."
    )
