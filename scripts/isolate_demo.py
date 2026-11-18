from sqlalchemy import update, select, func

from src.database.connection import SessionLocal
from src.database.models import BusinessOrder
from src.security.models import Company

with SessionLocal.begin() as session:
    companies = session.scalar(
        select(func.count()).select_from(Company)
    )

    if companies > 0:
        raise RuntimeError(
            "Companies already exist. Do not automatically "
            "reassign orders. Review tenant ownership manually."
        )

    result = session.execute(
        update(BusinessOrder)
        .where(BusinessOrder.tenant_id == 1)
        .values(tenant_id=0)
    )

    print(
        f"Moved {result.rowcount} demo orders "
        "to reserved tenant 0"
    )
