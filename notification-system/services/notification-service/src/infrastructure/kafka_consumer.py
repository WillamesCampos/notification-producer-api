import json
import asyncio
from aiokafka import AIOKafkaConsumer
from notification_service.config import settings, Logger
from notification_service.services.notification_service import notification_service


class LoggerKafkaConsumer(Logger):
    def __init__(self):
        super().__init__("notification_service.infrastructure.kafka_consumer")


logger = LoggerKafkaConsumer().logger
_consumer_task = None
_should_stop = False


async def start_consumer():
    global _consumer_task, _should_stop
    _should_stop = False

    # Create a task to consume events in background
    _consumer_task = asyncio.create_task(consume_events())
    logger.info(f"✅ Kafka Consumer started for topic: {settings.kafka_topic} and group: {settings.kafka_group_id}")


async def consume_events():

    global _should_stop

    consumer = AIOKafkaConsumer(
        settings.kafka_topic,
        bootstrap_servers=settings.kafka_bootstrap_servers,
        group_id=settings.kafka_group_id,
        value_deserializer=lambda v: json.loads(v.decode('utf-8')),
        auto_offset_reset='earliest',
        enable_auto_commit=True
    )

    await consumer.start()
    logger.info(f"✅ Kafka Consumer started for topic: {settings.kafka_topic} and group: {settings.kafka_group_id}")

    try:
        async for message in consumer:
            if _should_stop:
                break

            event = message.value
            logger.info(f"✅ Received event: {event.get('event_type')}: {event.get('event_id')}")
            await notification_service.save_notification(event)
            await consumer.commit()

    except Exception as e:
        logger.error(f"❌ Error consuming events: {e}")
    finally:
        await consumer.stop()
        logger.info(f"🔌 Kafka Consumer stopped for topic: {settings.kafka_topic} and group: {settings.kafka_group_id}")