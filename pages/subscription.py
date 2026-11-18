import streamlit as st

from src.dashboard import setup_page, apply_theme
from src.security.access import current_user
from src.billing.plans import PLANS
from src.billing.service import get_subscription

setup_page("Subscription Plans", "💳")
apply_theme()

user = current_user()
subscription = get_subscription(user["company_id"])

st.title("OpsPilot AI Plans")
st.caption("Manage your business analytics subscription")

st.info(
    f"Current plan: {subscription['plan'].title()} | "
    f"Status: {subscription['status'].title()}"
)

columns = st.columns(3)

for column, (plan_id, plan) in zip(
    columns, PLANS.items()
):
    with column:
        with st.container(border=True):
            st.subheader(plan["name"])

            price = plan["price_inr"]

            if price is None:
                st.markdown("### Custom Pricing")
            else:
                st.markdown(
                    f"### INR {price:,}/month"
                )

            order_limit = plan["max_orders"]
            user_limit = plan["max_users"]

            st.write(
                f"Orders: {order_limit or 'Unlimited'}"
            )
            st.write(
                f"Users: {user_limit or 'Unlimited'}"
            )

            st.write(
                "AI Copilot: "
                + ("Yes" if plan["ai_copilot"] else "No")
            )

            st.write(
                "PDF Reports: "
                + ("Yes" if plan["pdf_reports"] else "No")
            )

            if plan_id == subscription["plan"]:
                st.success("Current Plan")
            else:
                st.caption(
                    "Online checkout coming soon"
                )

st.warning(
    "Billing is not active. Plan upgrades are "
    "not available until secure payment verification "
    "and subscription provisioning are implemented."
)
