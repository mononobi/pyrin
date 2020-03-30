# -*- coding: utf-8 -*-
"""
security manager module.
"""

from pyrin.core.globals import LIST_TYPES
from pyrin.security.manager import SecurityManager as BaseSecurityManager

from tests.unit.security.permissions import PERMISSION_TEST_ONE, PERMISSION_TEST_TWO, \
    PERMISSION_TEST_THREE


class SecurityManager(BaseSecurityManager):
    """
    security manager class.
    """

    def has_permission(self, user, permissions, **options):
        """
        gets a value indicating that given user has the specified permissions.

        :param dict user: user identity to check its permissions.
        :param list[PermissionBase] permissions: permissions to check for user.

        :rtype: bool
        """

        required_permissions = permissions
        if not isinstance(permissions, LIST_TYPES):
            required_permissions = [permissions]

        needed_permissions = set(required_permissions)
        user_permissions = {PERMISSION_TEST_ONE,
                            PERMISSION_TEST_TWO,
                            PERMISSION_TEST_THREE}

        return needed_permissions.issubset(user_permissions)
