import pandas as pd
from sqlalchemy import select
from src.database.connection import SessionLocal
from src.database.models import BusinessOrder

def get_orders(tenant_id=1):
    with SessionLocal() as session:
        stmt = select(
            BusinessOrder.order_id,
            BusinessOrder.order_date,
            BusinessOrder.customer,
            BusinessOrder.site,
            BusinessOrder.product,
            BusinessOrder.quantity,
            BusinessOrder.price_per_unit,
            BusinessOrder.cost_per_unit
        ).where(
            BusinessOrder.tenant_id == tenant_id
        )

        rows = session.execute(stmt).mappings().all()

    df = pd.DataFrame([dict(row) for row in rows])

    if df.empty:
        return df

    df["order_date"] = pd.to_datetime(df["order_date"])

    for col in [
        "quantity", "price_per_unit", "cost_per_unit"
    ]:
        df[col] = pd.to_numeric(df[col])

    df["revenue"] = df["quantity"] * df["price_per_unit"]
    df["cost"] = df["quantity"] * df["cost_per_unit"]
    df["profit"] = df["revenue"] - df["cost"]

    return df
