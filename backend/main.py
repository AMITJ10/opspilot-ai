from fastapi import FastAPI, Response, status
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from backend.api.auth import router as auth_router
from src.database.connection import engine


app = FastAPI(
    title="OpsPilot AI API",
    description="Business Intelligence SaaS Backend",
    version="1.0.0",
)

app.include_router(auth_router)


@app.get("/")
def root():
    return {
        "application": "OpsPilot AI",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "opspilot-backend",
    }


@app.get("/health/database")
def database_health(response: Response):
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        return {
            "status": "connected",
            "database": "postgresql",
        }

    except SQLAlchemyError:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

        return {
            "status": "unavailable",
            "database": "postgresql",
        }
