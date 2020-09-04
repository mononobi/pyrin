# -*- coding: utf-8 -*-
"""
caching audit package.
"""

from pyrin.packaging.base import Package


class CachingAuditPackage(Package):
    """
    caching audit package class.
    """

    NAME = __name__
    COMPONENT_NAME = 'caching.audit.component'
    DEPENDS = ['pyrin.audit']
