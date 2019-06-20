from flask import Flask

from back.utils.config_class import BaseConfig, EnvironmentVariable, BoolEnvironmentVariable, IntEnvironmentVariable


class Config(BaseConfig):
    # App settings
    # --> General
    APP_NAME = "my-shops"
    ENVIRONMENT = EnvironmentVariable()
    TESTING = BoolEnvironmentVariable(default=False)
    # --> Security
    SECRET_KEY = EnvironmentVariable()
    BCRYPT_LOG_ROUNDS = IntEnvironmentVariable(default=4)
    BCRYPT_HANDLE_LONG_PASSWORDS = True

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

    def __init__(self) -> None:
        if self.TESTING:
            self.POSTGRES_DB = self.POSTGRES_DB_TEST
            self.LOGIN_DISABLED = True

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return "postgresql://{}:{}@{}:5432/{}".format(
            self.POSTGRES_USER, self.POSTGRES_PASSWORD, self.POSTGRES_HOST, self.POSTGRES_DB
        )


config = Config()


def init_app(app: Flask) -> None:
    app.config.from_object(config)
