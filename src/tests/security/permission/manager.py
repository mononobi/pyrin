# -*- coding: utf-8 -*-
"""
permission manager module.
"""

from pyrin.security.permission.manager import PermissionManager as BasePermissionManager


class TestPermissionManager(BasePermissionManager):
    """
    test permission manager class.
    """

    def synchronize_all(self, **options):
        """
        synchronizes all permissions with database.
        it creates or updates the available permissions.
        """
        pass
