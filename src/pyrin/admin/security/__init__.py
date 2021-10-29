# -*- coding: utf-8 -*-
"""
admin security package.
"""

from pyrin.packaging.base import Package


class AdminSecurityPackage(Package):
    """
    admin security package class.
    """

    NAME = __name__
    DEPENDS = ['pyrin.security.authentication.handlers',
               'pyrin.security.authorization.handlers']
