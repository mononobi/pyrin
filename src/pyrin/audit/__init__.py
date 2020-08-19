# -*- coding: utf-8 -*-
"""
audit package.
"""

from pyrin.packaging.base import Package


class AuditPackage(Package):
    """
    audit package class.
    """

    NAME = __name__
    DEPENDS = ['pyrin.api.router']
    COMPONENT_NAME = 'audit.component'
