from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from starlette import status
from notification_service.config import Logger
from notification_service.services.notification_service import notification_service


class LoggerAPI(Logger):
    def __init__(self):
        super().__init__("notification_service.api.routes")


logger = LoggerAPI().logger

router = APIRouter()


@router.get("/notifications/{user_id}")
async def get_notifications(
    user_id: str,
    limit: int = Query(default=10, ge=1, le=50, description="Number of notifications to return"),
    skip: int = Query(default=0, ge=0, description="Number of notifications to skip - pagination")):
    try:
        notifications = await notification_service.get_user_notifications(user_id, limit, skip)
        logger.info(f"✅ Notifications fetched successfully for user: {user_id}")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"user_id": user_id, "count": len(notifications), "notifications": notifications}
        )
    except Exception as e:
        logger.error(f"❌ Error fetching notifications for user: {user_id}: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.patch("/notifications/{event_id}/read")
async def mark_notification_as_read(
    event_id: str,
    user_id: str = Query(..., description="The ID of the user who is marking the notification as read")
):

    success = await notification_service.mark_as_read(event_id, user_id)

    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Notification not found")

    logger.info(f"✅ Notification marked as read: {event_id}")
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"status": "marked as read", "event_id": event_id}
    )