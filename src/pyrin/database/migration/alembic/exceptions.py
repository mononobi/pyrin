# -*- coding: utf-8 -*-
"""
database migration alembic exceptions module.
"""

from pyrin.core.exceptions import CoreException, CoreBusinessException


class DatabaseMigrationAlembicManagerException(CoreException):
    """
    database migration alembic manager exception.
    """
    pass


class DatabaseMigrationAlembicManagerBusinessException(CoreBusinessException,
                                                       DatabaseMigrationAlembicManagerException):
    """
    database migration alembic manager business exception.
    """
    pass
