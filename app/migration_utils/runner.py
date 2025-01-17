from typing import Any

from alembic.config import CommandLine, Config

from core.config import settings


def make_config() -> Config:
    """Create and configurate Alembic config object using project settings.

    Returns:
        Config: Alembic Config object
    """

    alembic_config = Config()
    alembic_config.set_main_option("script_location", settings.alembic.script_location)
    alembic_config.set_main_option(
        "version_locations", settings.alembic.version_locations
    )
    alembic_config.set_main_option(
        "sqlalchemy.url", settings.main_db.postgres_url.unicode_string()
    )
    alembic_config.set_main_option("file_template", settings.alembic.file_template)
    alembic_config.set_main_option("timezone", settings.alembic.timezone)

    return alembic_config


def alembic_runner(*args: Any) -> None:
    """Runs Alembic with given command line args and current configuration.

    Args:
        args (Any): Command line arguments.
    """

    cli = CommandLine()
    cli.run_cmd(make_config(), cli.parser.parse_args(args))
