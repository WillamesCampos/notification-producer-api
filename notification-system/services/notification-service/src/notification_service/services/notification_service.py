from datetime import datetime
from typing import List, Optional
from pymongo.errors import DuplicateKeyError

from notification_service.domain.models import Notification
from notification_service.infrastructure.database import get_collection
from notification_service.config import Logger


class NotificationService:
    def __init__(self, logger_instance: Logger):
        self.logger = logger_instance.logger

    def _get_collection(self):
        """Get the collection, ensuring the database has been initialized."""
        return get_collection()

    async def save_notification(self, event: dict) -> Optional[Notification]:
        timestamp = event.get("timestamp")
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))

        notification = Notification(
            event_id=event.get("event_id"),
            event_type=event.get("event_type"),
            user_id=event.get("user_id"),
            timestamp=timestamp,
            payload=event.get("payload", {}),
            read=False,
            created_at=datetime.utcnow()
        )

        try:
            collection = self._get_collection()
            result = await collection.insert_one(notification.model_dump())
            self.logger.info(f"✅ Notification saved successfully: {notification.event_id}: {notification.event_type}")
            return notification
        except DuplicateKeyError:
            # Idempotency: If the notification already exists, it will not be saved again
            self.logger.warning(f"⚠️ Notification already exists: {event.get('event_id')}")
            return None

    async def get_user_notifications(self, user_id: str, limit: int = 50, skip: int = 0) -> List[dict]:
        collection = self._get_collection()
        cursor = collection.find({"user_id": user_id}).sort("timestamp", -1).skip(skip).limit(limit)

        try:
            notifications = await cursor.to_list(length=limit)

            # Convert the MongoDB documents to dictionaries and remove the _id field
            for notif in notifications:
                notif.pop("_id", None)

            return notifications
        except Exception as e:
            self.logger.error(f"❌ Error getting user notifications: {e}", exc_info=True)
            return []

    async def mark_as_read(self, event_id: str, user_id: str) -> bool:
        try:
            collection = self._get_collection()
            result = await collection.update_one(
                {"event_id": event_id, "user_id": user_id},
                {"$set": {"read": True}}
            )
            if result.modified_count > 0:
                self.logger.info(f"✅ Notification marked as read: {event_id}")
                return True
            else:
                self.logger.warning(f"⚠️ Notification not found: {event_id}")
                return False
        except Exception as e:
            self.logger.error(f"❌ Error marking notification as read: {e}", exc_info=True)
            return False


class LoggerNotificationService(Logger):
    def __init__(self):
        super().__init__("notification_service.services.notification_service")


logger_instance = LoggerNotificationService()

notification_service = NotificationService(logger_instance)

