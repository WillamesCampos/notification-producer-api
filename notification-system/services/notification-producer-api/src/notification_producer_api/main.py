from fastapi import FastAPI

app = FastAPI(
    title="Notification Producer API",
    version="1.0.0",
    description="API for producing notifications",
)

@app.get("/health")
def health_check():
    return {"status": "ok", "service": "notification-producer-api"}

@app.get("/")
def root():
    return {"message": "Notification Producer API is running"}