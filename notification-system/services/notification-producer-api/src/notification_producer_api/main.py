from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette import status
from contextlib import asynccontextmanager
from notification_producer_api.infrastructure.kafka_producer import init_kafka_producer, close_kafka_producer
from notification_producer_api.api.routes import router as api_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_kafka_producer() # Startup Kafka Producer
    yield
    await close_kafka_producer() # Shutdown Kafka Producer


app = FastAPI(
    title="Notification Producer API",
    version="1.0.0",
    description="API for producing notifications",
    lifespan=lifespan,
)


app.include_router(api_router)


@app.get("/health")
def health_check():
    return JSONResponse(
        content={"status": "ok", "service": "notification-producer-api"},
        status_code=status.HTTP_200_OK,
        media_type="application/json"
    )

@app.get("/")
def root():
    return {"message": "Notification Producer API is running"}
