from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Notification(BaseModel):
    event_id: str = Field(..., description="The ID of the event that triggered the notification")
    event_type: str = Field(..., description="The type of event that triggered the notification")
    user_id: str = Field(..., description="The ID of the user that triggered the notification")
    timestamp: datetime = Field(..., description="The timestamp of the notification")
    payload: dict = Field(..., description="The payload of the notification")
    read: bool = Field(default=False, description="Whether the notification has been read")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="The timestamp of the notification creation")

    class Config:
        json_schema_extra = {
            "example": {
                "event_id": "ab-123-uuid",
                "event_type": "task.created",
                "user_id": "user-123-uuid",
                "timestamp": "2021-01-01T00:00:00Z",
                "payload": {"task_title": "Hello, world!"},
                "read": False,
                "created_at": "2021-01-01T00:00:00Z"
            }
        }

