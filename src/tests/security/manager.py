# -*- coding: utf-8 -*-
"""
security manager module.
"""

from pyrin.security.manager import SecurityManager

from tests.security.permissions import PERMISSION_TEST_ONE, PERMISSION_TEST_TWO, \
    PERMISSION_TEST_THREE


class TestSecurityManager(SecurityManager):
    """
    test security manager class.
    """

    def get_permission_ids(self, **options):
        """
        gets permission ids according to given inputs.

        :keyword dict user: user identity to get it's permission ids.

        :returns: list[permission_ids]

        :rtype: list
        """

        permission_ids = []
        permission_ids.extend([PERMISSION_TEST_ONE.get_id(),
                               PERMISSION_TEST_TWO.get_id(),
                               PERMISSION_TEST_THREE.get_id()])

        return permission_ids

    def is_active(self, user, **options):
        """
        gets a value indicating that given user is active.

        :param dict user: user to check is active.

        :rtype: bool
        """

        return user is not None
