# -*- coding: utf-8 -*-
"""
database audit package.
"""

from pyrin.packaging.base import Package


class DatabaseAuditPackage(Package):
    """
    database audit package class.
    """

    NAME = __name__
    COMPONENT_NAME = 'database.audit.component'
    DEPENDS = ['pyrin.audit']
