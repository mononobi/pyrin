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
    DEPENDS = ['pyrin.api.router',
               'pyrin.configuration']
    COMPONENT_NAME = 'audit.component'
    CONFIG_STORE_NAMES = ['audit']
