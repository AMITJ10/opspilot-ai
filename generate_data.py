import pandas as pd
import numpy as np

rng = np.random.default_rng(42)

n = 1800

df = pd.DataFrame({
    "order_id": [f"ORD{i:05d}" for i in range(1, n + 1)],
    "order_date": pd.date_range("2025-01-01", periods=n, freq="6h"),
    "customer": rng.choice(
        ["ABC Infra", "BuildTech", "Metro Projects", "Prime Construction"],
        n
    ),
    "site": rng.choice(
        ["Plant A", "Plant B", "Plant C"],
        n
    ),
    "product": rng.choice(
        ["M20 Concrete", "M25 Concrete", "M30 Concrete", "Aggregates"],
        n
    ),
    "quantity": rng.integers(5, 100, n),
    "price_per_unit": rng.integers(3500, 6500, n),
    "cost_per_unit": rng.integers(2500, 3500, n)
})

df.to_csv("data/sample_orders.csv", index=False)

print("Generated", len(df), "orders")
