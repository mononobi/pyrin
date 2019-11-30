# -*- coding: utf-8 -*-
"""
users manager module.
"""

from pyrin.security.users.manager import UsersManager


class TestUsersManager(UsersManager):
    """
    test users manager class.
    """

    def is_active(self, user, **options):
        """
        gets a value indicating that given user is active.

        :param dict user: user to check its active status.

        :rtype: bool
        """

        return user is not None
