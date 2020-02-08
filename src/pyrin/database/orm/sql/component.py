# -*- coding: utf-8 -*-
"""
database orm sql component module.
"""

from pyrin.application.decorators import component
from pyrin.application.context import Component
from pyrin.database.orm.sql import DatabaseORMSQLPackage
from pyrin.database.orm.sql.manager import DatabaseORMSQLManager


@component(DatabaseORMSQLPackage.COMPONENT_NAME)
class DatabaseORMSQLComponent(Component, DatabaseORMSQLManager):
    """
    database orm sql component class.
    """
    pass
