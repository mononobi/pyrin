# -*- coding: utf-8 -*-
"""
authorization handlers internal module.
"""

from pyrin.security.authorization.handlers.base import AuthorizerBase


class InternalAuthorizer(AuthorizerBase):
    """
    internal authorizer class.

    all application internal authorizers must be subclassed from this.
    for example admin, swagger or audit authorizers.
    """

    def _is_superuser(self, user, **options):
        """
        gets a value indicating that given internal user is superuser.

        :param int user: internal user id to be checked if it is superuser.

        :keyword dict user_info: internal user info to be used to check for user.

        :rtype: bool
        """

        user_info = options.get('user_info')
        return user_info and user_info.get('is_superuser') is True

    def _is_active(self, user, **options):
        """
        gets a value indicating that the given internal user is active.

        :param int user: internal user id to be checked if it is active.

        :keyword dict user_info: internal user info to be used to check for user.

        :rtype: bool
        """

        user_info = options.get('user_info')
        return user_info and user_info.get('is_active') is True
