from src.database.connection import Base, engine

from src.database import models
from src.security import models as security_models
from src.billing import models as billing_models

Base.metadata.create_all(bind=engine)

print("All database tables initialized successfully!")
