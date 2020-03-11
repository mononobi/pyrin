# -*- coding: utf-8 -*-
"""
permission package.
"""

from pyrin.security.permission import PermissionPackage as BasePermissionPackage


class PermissionPackage(BasePermissionPackage):
    """
    permission package class.
    """

    NAME = __name__
