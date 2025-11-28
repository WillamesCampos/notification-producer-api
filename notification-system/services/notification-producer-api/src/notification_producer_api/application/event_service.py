# import uuid
# from datetime import datetime
# from notification_producer_api.domain.events import (
#     EventMetadata,
#     EventPayload,
#     EventType,
#     NotificationEvent,
#     PublishEventRequest,
# )
# from notification_producer_api.infrastructure.kafka_producer import publish_event
# from notification_producer_api.config import logger


# class EventService:
#     """Service layer para lógica de publicação de eventos."""

#     @staticmethod
#     async def publish_notification_event(request: PublishEventRequest, topic: str) -> NotificationEvent:
#         """
#         Cria e publica um evento de notificação no Kafka.
        
#         Args:
#             request: Dados do evento a ser publicado
#             topic: Tópico do Kafka onde o evento será publicado
            
#         Returns:
#             NotificationEvent: Evento criado e publicado
            
#         Raises:
#             RuntimeError: Se o producer não estiver inicializado
#             Exception: Erros de publicação no Kafka
#         """
#         # Cria metadados do evento
#         metadata = EventMetadata(
#             event_id=str(uuid.uuid4()),
#             event_type=request.event_type,
#             timestamp=datetime.utcnow(),
#             correlation_id=request.correlation_id,
#             user_id=request.user_id,
#         )

#         # Cria payload
#         payload = EventPayload(data=request.payload)

#         # Monta evento completo
#         event = NotificationEvent(metadata=metadata, payload=payload)

#         # Publica no Kafka
#         try:
#             await publish_event(topic=topic, event=event.to_dict())
#             logger.info(
#                 f"Event published successfully",
#                 extra={
#                     "event_id": metadata.event_id,
#                     "event_type": request.event_type.value,
#                     "topic": topic,
#                 }
#             )
#         except Exception as e:
#             logger.error(
#                 f"Failed to publish event",
#                 extra={
#                     "event_id": metadata.event_id,
#                     "event_type": request.event_type.value,
#                     "topic": topic,
#                     "error": str(e),
#                 },
#                 exc_info=True,
#             )
#             raise

#         return event

