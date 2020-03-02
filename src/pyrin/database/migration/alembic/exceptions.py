# -*- coding: utf-8 -*-
"""
alembic exceptions module.
"""

from pyrin.core.exceptions import CoreException, CoreBusinessException


class AlembicManagerException(CoreException):
    """
    alembic manager exception.
    """
    pass


class AlembicManagerBusinessException(CoreBusinessException,
                                      AlembicManagerException):
    """
    alembic manager business exception.
    """
    pass
