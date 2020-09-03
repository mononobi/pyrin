# -*- coding: utf-8 -*-
"""
database bulk component module.
"""

from pyrin.application.decorators import component
from pyrin.application.structs import Component
from pyrin.database.bulk import DatabaseBulkPackage
from pyrin.database.bulk.manager import DatabaseBulkManager


@component(DatabaseBulkPackage.COMPONENT_NAME)
class DatabaseBulkComponent(Component, DatabaseBulkManager):
    """
    database bulk component class.
    """
    pass
