from pydantic import BaseModel, PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresDBConfig(BaseModel):
    """Main database connection settings model.

    Attributes:
        scheme (str): Scheme for build postgresdsn. "postgresql+asycnpg" by default

        db_user (str): Database user's name

        db_password (str): Database user's password

        db_host (str): Host to connect to database

        db_port (int): Port to connect to database

        db_name (str): Database name

        cho_sql (bool): Logging sql statesments. "True" by default

        echo_pool (bool): Logging connection pool information. "True" by default

        pool_size (int): The number of connections to keep open inside the connection
        pool. 40 by default

        max_overflow (int): The number of connections to allow in connection pool
        overflow. 10 by default

        naming_convention (dict): Naming conventions to use in database migrations

    Properties:
        postgres_url (PostgresDsn): Postgres url built from db settings.
    """

    scheme: str = "postgresql+asyncpg"
    db_user: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str
    echo_sql: bool = True
    echo_pool: bool = True
    pool_size: int = 40
    max_overflow: int = 10
    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @computed_field
    @property
    def postgres_url(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme=self.scheme,
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            path=self.db_name,
        )


class Settings(BaseSettings):
    """A base class for app's settings. Settings values might be overriden by
    environment variables.

    Attributes:
        main_db (PostgresDBConfig): Main database connection settings model

        model_config (SettingsConfigDict): Settings configuration
    """

    main_db: PostgresDBConfig

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=(".env", "app/.env"),
        env_nested_delimiter="__",
        env_prefix="CONFIG__",
    )


settings = Settings()