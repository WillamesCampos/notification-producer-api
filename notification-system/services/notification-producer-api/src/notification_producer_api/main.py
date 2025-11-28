from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette import status

app = FastAPI(
    title="Notification Producer API",
    version="1.0.0",
    description="API for producing notifications",
)

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