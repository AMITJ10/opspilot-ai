import streamlit as st
import pandas as pd

from sqlalchemy.dialects.postgresql import insert

from src.dashboard import setup_page, apply_theme
from src.security.access import require_role
from src.database.connection import SessionLocal
from src.database.models import BusinessOrder

setup_page("Data Hub", "📁")
apply_theme()

user = require_role("owner", "admin")

st.title("Data Hub")
st.caption(
    f"Import business data for {user['company_name']}"
)

uploaded = st.file_uploader(
    "Upload Orders CSV",
    type=["csv"]
)

required = {
    "order_id",
    "order_date",
    "customer",
    "site",
    "product",
    "quantity",
    "price_per_unit",
    "cost_per_unit"
}

if uploaded is not None:
    if uploaded.size > 10 * 1024 * 1024:
        st.error("Maximum upload size is 10 MB")
        st.stop()

    try:
        df = pd.read_csv(uploaded)

        missing = required - set(df.columns)

        if missing:
            st.error(
                f"Missing columns: {sorted(missing)}"
            )
            st.stop()

        df = df[list(sorted(required))].copy()

        df["order_date"] = pd.to_datetime(
            df["order_date"],
            errors="coerce"
        )

        numeric = [
            "quantity",
            "price_per_unit",
            "cost_per_unit"
        ]

        for col in numeric:
            df[col] = pd.to_numeric(
                df[col], errors="coerce"
            )

        df = df.dropna(subset=list(required))

        df = df.drop_duplicates(
            subset=["order_id"],
            keep="last"
        )

        df = df[
            (df["quantity"] > 0)
            & (df["price_per_unit"] >= 0)
            & (df["cost_per_unit"] >= 0)
        ].copy()

        if df.empty:
            st.error("No valid orders found")
            st.stop()

        st.success(
            f"{len(df)} valid records ready"
        )

        st.dataframe(
            df.head(20),
            use_container_width=True
        )

        if st.button("Import to PostgreSQL"):
            records = []

            for row in df.to_dict("records"):
                records.append({
                    "tenant_id": user["company_id"],
                    "order_id": str(row["order_id"]),
                    "order_date": row["order_date"].to_pydatetime(),
                    "customer": str(row["customer"]),
                    "site": str(row["site"]),
                    "product": str(row["product"]),
                    "quantity": float(row["quantity"]),
                    "price_per_unit": float(row["price_per_unit"]),
                    "cost_per_unit": float(row["cost_per_unit"])
                })

            with SessionLocal.begin() as session:
                stmt = insert(BusinessOrder).values(records)

                stmt = stmt.on_conflict_do_nothing(
                    constraint="uq_tenant_order"
                )

                result = session.execute(stmt)

            st.cache_data.clear()
            st.success(
                f"Import completed. {result.rowcount} new orders."
            )

    except Exception as exc:
        st.error(f"Import failed: {exc}")
