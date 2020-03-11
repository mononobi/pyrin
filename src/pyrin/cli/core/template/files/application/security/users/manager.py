# -*- coding: utf-8 -*-
"""
users manager module.
"""

from pyrin.security.users.manager import UsersManager as BaseUsersManager
from pyrin.core.exceptions import CoreNotImplementedError


class UsersManager(BaseUsersManager):
    """
    users manager class.
    """

    def is_active(self, user, **options):
        """
        gets a value indicating that given user is active.

        :param user: user to check its active status.

        :rtype: bool
        """

        raise CoreNotImplementedError()
