import os
import pytest
from sqlalchemy import create_engine, text


APP_DATABASE_URL = os.getenv("APP_DATABASE_URL")


@pytest.mark.skipif(
    not APP_DATABASE_URL,
    reason="APP_DATABASE_URL not configured"
)
def test_tenant_isolation():
    engine = create_engine(APP_DATABASE_URL)

    with engine.connect() as conn:
        role = conn.execute(
            text("SELECT current_user")
        ).scalar_one()

        assert role == "opspilot_app"

        conn.rollback()

        with conn.begin():
            count_without_context = conn.execute(
                text("SELECT COUNT(*) FROM business_orders")
            ).scalar_one()

            assert count_without_context == 0

        with conn.begin():
            conn.execute(
                text(
                    "SELECT set_config("
                    "'app.tenant_id', '1', true)"
                )
            )

            tenant_1 = conn.execute(
                text(
                    "SELECT COUNT(*) FROM business_orders "
                    "WHERE tenant_id <> 1"
                )
            ).scalar_one()

            assert tenant_1 == 0

        with conn.begin():
            conn.execute(
                text(
                    "SELECT set_config("
                    "'app.tenant_id', '2', true)"
                )
            )

            tenant_2 = conn.execute(
                text(
                    "SELECT COUNT(*) FROM business_orders "
                    "WHERE tenant_id <> 2"
                )
            ).scalar_one()

            assert tenant_2 == 0

    engine.dispose()
