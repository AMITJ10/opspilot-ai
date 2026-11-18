import pandas as pd
from sqlalchemy import select
from src.database.connection import SessionLocal
from src.database.models import BusinessOrder

CSV_PATH = "data/sample_orders.csv"
TENANT_ID = 1

df = pd.read_csv(CSV_PATH)

required = [
    "order_date", "customer", "site",
    "quantity", "price_per_unit", "cost_per_unit"
]

missing = set(required) - set(df.columns)

if missing:
    raise ValueError(f"Missing columns: {sorted(missing)}")

if "order_id" not in df.columns:
    df["order_id"] = [
        f"DEMO-{i:06d}" for i in range(1, len(df) + 1)
    ]

if "product" not in df.columns:
    df["product"] = "General Product"

df["order_date"] = pd.to_datetime(
    df["order_date"], errors="coerce"
)

for col in ["quantity", "price_per_unit", "cost_per_unit"]:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(
    subset=required + ["order_id", "product"]
).copy()

if df["order_id"].duplicated().any():
    raise ValueError("Duplicate order IDs found in CSV")

if (
    (df["quantity"] <= 0)
    | (df["price_per_unit"] < 0)
    | (df["cost_per_unit"] < 0)
).any():
    raise ValueError("Invalid quantity or price values")

with SessionLocal.begin() as session:
    existing_ids = set(
        session.scalars(
            select(BusinessOrder.order_id).where(
                BusinessOrder.tenant_id == TENANT_ID
            )
        ).all()
    )

    records = []

    for row in df.itertuples(index=False):
        order_id = str(row.order_id)

        if order_id in existing_ids:
            continue

        records.append(
            BusinessOrder(
                tenant_id=TENANT_ID,
                order_id=order_id,
                order_date=row.order_date.to_pydatetime(),
                customer=str(row.customer),
                site=str(row.site),
                product=str(row.product),
                quantity=float(row.quantity),
                price_per_unit=float(row.price_per_unit),
                cost_per_unit=float(row.cost_per_unit)
            )
        )

    session.add_all(records)

print(f"Imported {len(records)} new orders")
