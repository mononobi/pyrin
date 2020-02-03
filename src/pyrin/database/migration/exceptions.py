# -*- coding: utf-8 -*-
"""
database migration exceptions module.
"""

from pyrin.core.exceptions import CoreException


class DatabaseMigrationManagerException(CoreException):
    """
    database migration manager exception.
    """
    pass


class EngineBindNameNotFoundError(DatabaseMigrationManagerException):
    """
    engine bind name not found error.
    """
    pass
