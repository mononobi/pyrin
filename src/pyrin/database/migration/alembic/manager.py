# -*- coding: utf-8 -*-
"""
alembic manager module.
"""

from pyrin.cli.mixin.handler import CLIMixin
from pyrin.core.context import Manager
from pyrin.database.migration.alembic.interface import AlembicCLIHandlerBase


class AlembicManager(Manager, CLIMixin):
    """
    alembic manager class.
    """

    _cli_handler_type = AlembicCLIHandlerBase
