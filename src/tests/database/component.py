# -*- coding: utf-8 -*-
"""
database component module.
"""

from pyrin.application.decorators import component
from pyrin.application.context import Component

from tests.database import TestDatabasePackage
from tests.database.manager import TestDatabaseManager


@component(TestDatabasePackage.COMPONENT_NAME, replace=True)
class TestDatabaseComponent(Component, TestDatabaseManager):
    """
    test database component class.
    """
