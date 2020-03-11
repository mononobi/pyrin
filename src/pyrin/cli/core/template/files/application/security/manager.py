# -*- coding: utf-8 -*-
"""
security manager module.
"""

from pyrin.security.manager import SecurityManager as BaseSecurityManager
from pyrin.core.exceptions import CoreNotImplementedError


class SecurityManager(BaseSecurityManager):
    """
    security manager class.
    """

    def has_permission(self, user, permissions, **options):
        """
        gets a value indicating that given user has the specified permissions.

        :param user: user identity to check its permissions.
        :param list[Permission] permissions: permissions to check for user.

        :rtype: bool
        """

        raise CoreNotImplementedError()
