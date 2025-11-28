import json
import asyncio
from typing import Optional
from aiokafka import AIOKafkaProducer
from notification_producer_api.config import settings, logger



_producer: Optional[AIOKafkaProducer] = None


async def init_kafka_producer() -> AIOKafkaProducer:
    global _producer


    max_retries = 3
    retry_delay = 5

    for attempt in range(max_retries):
        try:
            _producer = AIOKafkaProducer(bootstrap_servers=settings.kafka_bootstrap_servers, value_serializer=lambda v: json.dumps(v).encode("utf-8"))
            await _producer.start()
            logger.info(f"✅ Kafka Producer conectado em {settings.kafka_bootstrap_servers}")
            return _producer
        except Exception as e:
            if attempt < max_retries - 1:
                logger.warning(
                    f"⚠️ Tentativa {attempt + 1}/{max_retries} falhou. "
                    f"Kafka pode ainda estar inicializando. Aguardando {retry_delay}s..."
                )
                await asyncio.sleep(retry_delay)
            else:
                logger.error(f"❌ Erro ao conectar ao Kafka: {str(e)}")
                raise


async def close_kafka_producer() -> None:
    global _producer
    if _producer:
        await _producer.stop()
        _producer = None
        logger.info("❌ Kafka Producer disconnected")


async def publish_event(topic: str, event: dict) -> None:
    if _producer is None:
        raise RuntimeError("Kafka producer not initialized")

    try:
        # Use named parameters and capture the RecordMetadata
        record_metadata = await _producer.send_and_wait(
            topic=topic,
            value=event  # value_serializer will serialize automatically
        )

        logger.info(
            f"✅ Event published to '{topic}' "
            f"[partition={record_metadata.partition}, offset={record_metadata.offset}]: "
            f"{event.get('event_type', 'unknown')}"
        )
    except Exception as e:
        logger.error(f"❌ Error publishing event: {str(e)}", exc_info=True)
        raise