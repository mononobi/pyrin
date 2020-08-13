# -*- coding: utf-8 -*-
"""
alembic manager module.
"""

import pyrin.template.services as template_services

from pyrin.cli.mixin.handler import CLIMixin
from pyrin.core.structs import Manager
from pyrin.database.migration.alembic import AlembicPackage
from pyrin.database.migration.alembic.enumerations import AlembicCLIHandlersEnum
from pyrin.database.migration.alembic.interface import AlembicCLIHandlerBase


class AlembicManager(Manager, CLIMixin):
    """
    alembic manager class.
    """

    _cli_handler_type = AlembicCLIHandlerBase
    package_class = AlembicPackage

    def enable(self):
        """
        enables migrations for the application.
        """

        return template_services.create(AlembicCLIHandlersEnum.ENABLE)
