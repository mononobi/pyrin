# -*- coding: utf-8 -*-
"""
database paging component module.
"""

from pyrin.application.decorators import component
from pyrin.application.structs import Component
from pyrin.database.paging import DatabasePagingPackage
from pyrin.database.paging.manager import DatabasePagingManager


@component(DatabasePagingPackage.COMPONENT_NAME)
class DatabasePagingComponent(Component, DatabasePagingManager):
    """
    database paging component class.
    """
    pass
