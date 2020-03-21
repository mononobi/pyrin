# -*- coding: utf-8 -*-
"""
database component module.
"""

from pyrin.application.decorators import component
from pyrin.database import DatabasePackage
from pyrin.database.manager import DatabaseManager
from pyrin.application.structs import Component


@component(DatabasePackage.COMPONENT_NAME)
class DatabaseComponent(Component, DatabaseManager):
    """
    database component class.
    """
    pass
