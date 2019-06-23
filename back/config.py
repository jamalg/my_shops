from datetime import timedelta

from flask import Flask

from back.utils.config_class import BaseConfig, EnvironmentVariable, BoolEnvironmentVariable, IntEnvironmentVariable


class Config(BaseConfig):
    # App settings
    # --> General
    APP_NAME = "my-shops"
    SERVER_NAME = EnvironmentVariable()
    ENVIRONMENT = EnvironmentVariable()
    TESTING = BoolEnvironmentVariable(default=False)
    # --> Security
    SECRET_KEY = EnvironmentVariable()
    BCRYPT_LOG_ROUNDS = IntEnvironmentVariable(default=4)
    BCRYPT_HANDLE_LONG_PASSWORDS = True
    # --> Social
    DISLIKE_EXPIRY = timedelta(minutes=120)

    # External Services
    # --> DB
    POSTGRES_USER = EnvironmentVariable()
    POSTGRES_PASSWORD = EnvironmentVariable()
    POSTGRES_DB = EnvironmentVariable()
    POSTGRES_DB_TEST = EnvironmentVariable()
    POSTGRES_HOST = EnvironmentVariable()
    # --> Google Place API
    GOOGLE_CLOUD_API_KEY = EnvironmentVariable()
    GOOGLE_CLOUD_DEFAULT_OUTPUT = "json"
    GOOGLE_PHOTO_MAX_HEIGHT = 300
    MAX_THREAD_POOL_SIZE = 25
    DEFAULT_NEARBY_RADIUS = 1500
    DEFAULT_NEARBY_TYPE = "store"
    # --> Redis
    REDIS_HOST = EnvironmentVariable()
    REDIS_PORT = IntEnvironmentVariable(default=6379)
    REDIS_DB = IntEnvironmentVariable(default=0)
    NEARBY_PLACE_TTL = timedelta(days=7)
    PLACE_TTL = timedelta(days=7)
    PHOTO_TTL = timedelta(days=30)

    def __init__(self) -> None:
        if self.TESTING:
            self.POSTGRES_DB = self.POSTGRES_DB_TEST
            self.REDIS_DB = 1
            self.LOGIN_DISABLED = True

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return "postgresql://{}:{}@{}:5432/{}".format(
            self.POSTGRES_USER, self.POSTGRES_PASSWORD, self.POSTGRES_HOST, self.POSTGRES_DB
        )


config = Config()


def init_app(app: Flask) -> None:
    app.config.from_object(config)
