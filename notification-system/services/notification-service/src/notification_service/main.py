from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from starlette import status

from notification_service.config import settings, logger
from notification_service.infrastructure.kafka_consumer import start_consumer, stop_consumer
from notification_service.infrastructure.database import init_database, close_database
from notification_service.api.routes import router as api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting notification-service...")
    await init_database()
    await start_consumer()
    yield

    logger.info("Stopping notification-service...")
    await stop_consumer()
    await close_database()
    logger.info("🔴 Notification-service stopped")


app = FastAPI(
    title="Notification Service",
    version="0.1.0",
    description="Notification Service who consumes events from Kafka and stores them in MongoDB",
    lifespan=lifespan,
)

app.include_router(api_router)


@app.get("/health")
async def health_check():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "ok", "service": "notification-service"}
    )


@app.get("/")
def root():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Notification Service is running"}
    )

