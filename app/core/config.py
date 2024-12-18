from pydantic import BaseModel, PostgresDsn, computed_field
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    """A class for app running settings.

    Attributes:
        app (str): Entrypoint to start fastapi app by uvicorn
        host (str): Host to start app on
        port (int): Port to start app on
        auto_reload (bool): Auto reload app
    """

    app: str
    host: str
    port: int
    auto_reload: bool


class ApiPrefix(BaseModel):
    """A class for api prefixes configuration.

    Attributes:
        api_prefix (str): An api url prefix. Defaults to "/api"

        auth (str): Auth url prefix. Defaults to "/auth"

        users (str): Url prefix for users routes. Defaults to "/users"
    """

    api_prefix: str = "/api"
    users: str = "/users"
    auth: str = "/auth"

    @computed_field
    @property
    def get_bearer_token_url(self) -> str:
        """Builds string for bearer transport token url.

        Returns:
            str: token url. Formate: "api/auth/login"
        """
        return f"{self.api_prefix}{self.auth}/login"[1:]


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


class AlembicConfig(BaseModel):
    """A class for alembic settings.

    Attributes:
        script_location (str): Location for alembic script. "migration/utils/alembic" by
        default

        version_locations (str): Locatin for vesions files. "" by default

        file_template (str): A template for vesion file's names
        "%%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s"
        by default

        timezone (str): Alembic timezone: "UTC" by default
    """

    script_location: str = "migration_utils/alembic"
    version_locations: str = ""
    file_template: str = (
        "%%(year)d_%%(month).2d_%%(day).2d_%%(hour).2d%%(minute).2d-%%(rev)s_%%(slug)s"
    )
    timezone: str = "UTC"


class AccessTokenConfig(BaseModel):
    """A class for access token settings.

    Args:
        lifetime_seconds (int): Lifetime of the token

        reset_password_token_secret (str): Secret string for reset password

        verification_token_secret (str): Secret string for verification token
    """

    lifetime_seconds: int = 3600
    reset_password_token_secret: str
    verification_token_secret: str


class Settings(BaseSettings):
    """A base class for app's settings. Settings values might be overriden by
    environment variables.

    Attributes:
        alembic (AlembicConfig): Alembic configuration settings model

        prefix (ApiPrefix): Api prefixes configuration settings model

        access_token (AccessTokenConfig): Access token settings model

        run (RunConfig): Running application settings model

        main_db (PostgresDBConfig): Main database connection settings model

        model_config (SettingsConfigDict): Settings configuration
    """

    alembic: AlembicConfig = AlembicConfig()
    prefix: ApiPrefix = ApiPrefix()
    access_token: AccessTokenConfig
    run: RunConfig
    main_db: PostgresDBConfig

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file=(".env", "app/.env"),
        env_nested_delimiter="__",
        env_prefix="CONFIG__",
    )


settings = Settings()
