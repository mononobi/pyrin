# -*- coding: utf-8 -*-
"""
database component module.
"""

from pyrin.application.decorators import component
from pyrin.application.context import Component

from tests.database import DatabasePackage
from tests.database.manager import DatabaseManager


@component(DatabasePackage.COMPONENT_NAME, replace=True)
class DatabaseComponent(Component, DatabaseManager):
    """
    database component class.
    """
    pass
