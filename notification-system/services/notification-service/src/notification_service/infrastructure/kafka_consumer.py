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
    logger.info(f"✅ Kafka Consumer task started for topic: {settings.kafka_topic} and group: {settings.kafka_group_id}")


async def stop_consumer():
    global _consumer_task, _should_stop
    _should_stop = True

    if _consumer_task:
        _consumer_task.cancel()
        try:
            await _consumer_task
        except asyncio.CancelledError:
            pass
    logger.info("🔌 Kafka Consumer stopped")


async def consume_events():
    global _should_stop

    max_retries = 10
    retry_delay = 3  # seconds

    consumer = None

    # Retry logic to connect to Kafka
    for attempt in range(max_retries):
        try:
            consumer = AIOKafkaConsumer(
                settings.kafka_topic,
                bootstrap_servers=settings.kafka_bootstrap_servers,
                group_id=settings.kafka_group_id,
                value_deserializer=lambda v: json.loads(v.decode('utf-8')),
                auto_offset_reset='earliest',
                enable_auto_commit=True
            )

            await consumer.start()
            logger.info(f"✅ Kafka Consumer connected for topic: {settings.kafka_topic} and group: {settings.kafka_group_id}")
            break  # Success, exit the loop

        except Exception as e:
            if attempt < max_retries - 1:
                # There are still attempts, wait and try again
                logger.warning(
                    f"⚠️ Attempt {attempt + 1}/{max_retries} failed to connect to Kafka. "
                    f"Kafka may still be initializing. Waiting {retry_delay}s..."
                )
                await asyncio.sleep(retry_delay)
                # Clear the consumer before trying again
                if consumer:
                    try:
                        await consumer.stop()
                    except:
                        pass
                    consumer = None
            else:
                # Last attempt failed
                logger.error(f"❌ Failed to connect to Kafka after {max_retries} attempts. Consumer will not start.")
                if consumer:
                    try:
                        await consumer.stop()
                    except:
                        pass
                return  # Return without raising an exception

    # Check if consumer was initialized
    if consumer is None:
        logger.error("❌ Consumer not initialized. Aborting event consumption.")
        return

    # Check if consumer is really ready
    if not hasattr(consumer, '_client') or consumer._client is None:
        logger.error("❌ Consumer not fully initialized. Aborting.")
        try:
            await consumer.stop()
        except:
            pass
        return

    # Consumer connected successfully, start consuming events
    try:
        async for message in consumer:
            if _should_stop:
                break

            event = message.value
            logger.info(f"✅ Received event: {event.get('event_type')}: {event.get('event_id')}")
            await notification_service.save_notification(event)
            await consumer.commit()

    except asyncio.CancelledError:
        logger.info("🛑 Consumer task cancelled")
    except Exception as e:
        logger.error(f"❌ Error consuming events: {e}", exc_info=True)
    finally:
        if consumer:
            try:
                await consumer.stop()
                logger.info(f"🔌 Kafka Consumer stopped for topic: {settings.kafka_topic} and group: {settings.kafka_group_id}")
            except Exception as e:
                logger.error(f"❌ Error stopping consumer: {e}", exc_info=True)

