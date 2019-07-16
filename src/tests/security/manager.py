# -*- coding: utf-8 -*-
"""
security manager module.
"""

from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.security.manager import SecurityManager


class TestSecurityManager(SecurityManager):
    """
    test security manager class.
    """

    def get_permission_ids(self, **options):
        """
        gets permission ids according to given inputs.

        :keyword dict user: user identity to get it's permission ids.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: list[permission_ids]

        :rtype: list[object]
        """

        raise CoreNotImplementedError()

    def is_active(self, user, **options):
        """
        gets a value indicating that given user is active.

        :param dict user: user to check is active.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: bool
        """

        raise CoreNotImplementedError()
