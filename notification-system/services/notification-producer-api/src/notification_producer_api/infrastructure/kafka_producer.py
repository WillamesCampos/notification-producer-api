import json
import os
from typing import Optional
from aiokafka import AIOKafkaProducer
from notification_producer_api.config import settings, logger



_producer: Optional[AIOKafkaProducer] = None


async def init_kafka_producer() -> AIOKafkaProducer:
    global _producer

    _producer = AIOKafkaProducer(
        bootstrap_servers=settings.kafka_bootstrap_servers,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )
    await _producer.start()
    logger.info(f"✅ Kafka Producer conectado em {settings.kafka_bootstrap_servers}")


async def close_kafka_producer() -> None:
    global _producer
    if _producer:
        await _producer.stop()
        _producer = None
        logger.info("❌ Kafka Producer disconnected")


async def publish_event(topic: str, event: dict) -> None:
    if _producer is None:
        raise RuntimeError("Kafka producer not initialized")

    await _producer.send_and_wait(topic, event)
    logger.info(f"✅ Event has been published to '{topic}': {event.get('event_type', 'unknown')}")