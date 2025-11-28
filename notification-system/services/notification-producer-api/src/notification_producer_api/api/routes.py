from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from datetime import datetime
import uuid

from notification_producer_api.infrastructure.kafka_producer import publish_event
from notification_producer_api.domain.events import EventRequest, EventType
from notification_producer_api.config import logger


router = APIRouter(prefix="/api/v1")

@router.post("/events")
async def create_event(request: EventRequest):

    event = {
        "event_id": str(uuid.uuid4()),
        "event_type": request.event_type,
        "user_id": request.user_id,
        "payload": request.payload,
        "timestamp": datetime.utcnow().isoformat(),
    }

    try:
        await publish_event(topic="notifications", event=event)

        return JSONResponse(
            status_code=status.HTTP_202_ACCEPTED,
            content={
                "event_id": event["event_id"],
                "event_type": event["event_type"],
                "timestamp": event["timestamp"],
                "status": "success",
            },
        )
    except Exception as e:
        logger.error(f"Unexpected error publishing event: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to publish event: {str(e)}",
        )

@router.get("/events/types")
async def list_event_types():
    return {
        "event_types": [event_type.value for event_type in EventType],
        "description": "Supported event types for notification system",
    }

