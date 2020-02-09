# -*- coding: utf-8 -*-
"""
database migration alembic manager module.
"""

from pyrin.cli.mixin import CLIMixin
from pyrin.core.context import Manager
from pyrin.database.migration.alembic.interface import AlembicCLIHandlerBase


class DatabaseMigrationAlembicManager(Manager, CLIMixin):
    """
    database migration alembic manager class.
    """

    _cli_handler_type = AlembicCLIHandlerBase
