# -*- coding: utf-8 -*-
"""
alembic component module.
"""

from pyrin.application.decorators import component
from pyrin.database.migration.alembic import AlembicPackage
from pyrin.database.migration.alembic.manager import AlembicManager
from pyrin.application.structs import Component


@component(AlembicPackage.COMPONENT_NAME)
class AlembicComponent(Component, AlembicManager):
    """
    alembic component class.
    """
    pass
