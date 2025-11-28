from datetime import datetime
from enum import Enum
from typing import Any, Optional
from pydantic import BaseModel, Field, field_validator


class EventType(str, Enum):
    """Tipos de eventos suportados pelo sistema."""
    NOTIFICATION_CREATED = "notification.created"
    NOTIFICATION_SENT = "notification.sent"
    NOTIFICATION_FAILED = "notification.failed"
    USER_REGISTERED = "user.registered"
    USER_UPDATED = "user.updated"


class EventRequest(BaseModel):
    event_type: EventType = Field(..., description="Tipo do evento")
    user_id: str = Field(..., description="ID do usuário relacionado ao evento")
    payload: dict = Field(..., description="Dados do evento")


