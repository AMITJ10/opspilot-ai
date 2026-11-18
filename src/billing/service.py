from sqlalchemy import select

from src.database.connection import SessionLocal
from src.billing.models import Subscription
from src.billing.plans import PLANS


def get_subscription(company_id):
    with SessionLocal() as session:
        subscription = session.scalar(
            select(Subscription).where(
                Subscription.company_id == company_id
            )
        )

        if subscription is None:
            return {
                "plan": "starter",
                "status": "trial"
            }

        return {
            "plan": subscription.plan,
            "status": subscription.status
        }


def get_entitlements(company_id):
    subscription = get_subscription(company_id)

    plan = subscription["plan"]

    if plan not in PLANS:
        raise ValueError("Unknown subscription plan")

    if subscription["status"] not in {
        "trial", "active"
    }:
        return {
            **PLANS["starter"],
            "ai_copilot": False,
            "pdf_reports": False
        }

    return PLANS[plan]


def require_feature(company_id, feature):
    entitlements = get_entitlements(company_id)

    if not entitlements.get(feature, False):
        raise PermissionError(
            "This feature is not available on "
            "your current subscription."
        )
