from pydantic import BaseModel, PostgresDsn, StringConstraints, computed_field, constr
from pydantic_core import MultiHostUrl
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Annotated


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

        structures (str): Url prefix for structures routes. Defaults to "/structures"

        teams (str): Url prefix for teams routes. Defaults to "/teams"
    """

    api_prefix: str = "/api"
    users: str = "/users"
    auth: str = "/auth"
    structures: str = "/structures"
    teams: str = "/teams"

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

    Attributes:
        lifetime_seconds (int): Lifetime of the token

        reset_password_token_secret (str): Secret string for reset password

        verification_token_secret (str): Secret string for verification token
    """

    lifetime_seconds: int = 3600
    reset_password_token_secret: str
    verification_token_secret: str


class SuperUserConfig(BaseModel):
    """A class with superuser credentials for create superuser script.

    Attributes:
        email (str): Superuser's  email
        password (str): Superuser's password
        name (str): Name for superuser
        last_name (str): Last name for superuser
        info (str): Addictional info for superuser. Defaults to None
        is_active (bool): Superuser's active status. Defaults to "True"
        is_superuser (bool): Superuser's superuser status. Defaults to "True"
        is_verified (bool): Superuser's verified status. Defaults to "True"
    """

    email: str
    password: str
    name: Annotated[str, StringConstraints(max_length=60)]
    last_name: Annotated[str, StringConstraints(max_length=60)]
    info: str | None = None
    is_active: bool = True
    is_superuser: bool = True
    is_verified: bool = True


class RedisConfig(BaseModel):
    """A class for redis connection settings.

    Attributes:
        user (str): Redis user name
        password (str): Redis user password
        host (str): Host to connect
        port (int): Port to connect
        db (int): Redis database to connect
    """

    user: str
    password: str
    host: str
    port: int
    db: int


class SessionMiddlewareConfig(BaseModel):
    """A class for session middleware settings using in starlette-admin.

    Attributes:
        secret_key (str): Secret key for session middleware
    """

    secret_key: str


class Settings(BaseSettings):
    """A base class for app's settings. Settings values might be overriden by
    environment variables.

    Attributes:
        alembic (AlembicConfig): Alembic configuration settings model

        prefix (ApiPrefix): Api prefixes configuration settings model

        session_middleware (SessionMiddlewareConfig): SessionMiddlware settings model

        superuser (SuperUserConfig): Superusers credentials settings model

        access_token (AccessTokenConfig): Access token settings model

        run (RunConfig): Running application settings model

        main_db (PostgresDBConfig): Main database connection settings model

        model_config (SettingsConfigDict): Settings configuration
    """

    alembic: AlembicConfig = AlembicConfig()
    prefix: ApiPrefix = ApiPrefix()
    session_middleware: SessionMiddlewareConfig
    redis: RedisConfig
    superuser: SuperUserConfig
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
