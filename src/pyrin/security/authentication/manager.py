# -*- coding: utf-8 -*-
"""
authentication manager module.
"""

from pyrin.core.context import CoreObject


class AuthenticationManager(CoreObject):
    """
    authentication manager class.
    this class is intended to be an interface for top level application's authentication
    package, so most methods of this class will raise CoreNotImplementedError.
    """

    def login(self, username, encrypted_password, **options):
        """
        logs in the specified user with given credentials.

        :param str username: username.
        :param str encrypted_password: encrypted password of user.

        :returns: token

        :rtype: str
        """
        pass
