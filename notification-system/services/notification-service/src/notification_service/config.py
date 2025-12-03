import logging
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # MongoDB settings
    mongodb_uri: str = "mongodb://localhost:27017"
    mongodb_database: str = "notifications_db"
    mongodb_collection: str = "notifications"
    
    # Kafka settings
    kafka_topic: str = "notifications"
    kafka_bootstrap_servers: list[str] = ["localhost:9092"]
    kafka_group_id: str = "notification-service-group"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )


settings = Settings()


class Logger:
    def __init__(self, name: str = "notification-service"):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        self.logger = logging.getLogger(name)


logger = Logger().logger

