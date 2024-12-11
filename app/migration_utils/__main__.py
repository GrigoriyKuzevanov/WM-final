import sys

from .runner import alembic_runner

alembic_runner(*sys.argv[1:])
