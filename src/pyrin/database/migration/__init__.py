# -*- coding: utf-8 -*-
"""
database migration package.
"""

from pyrin.packaging.base import Package


class DatabaseMigrationPackage(Package):
    """
    database migration package class.
    """

    NAME = __name__
    COMPONENT_NAME = 'database.migration.component'
