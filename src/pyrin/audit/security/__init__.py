# -*- coding: utf-8 -*-
"""
audit security package.
"""

from pyrin.packaging.base import Package


class AuditSecurityPackage(Package):
    """
    audit security package class.
    """

    NAME = __name__
    DEPENDS = ['pyrin.security.authentication.handlers',
               'pyrin.security.authorization.handlers']
