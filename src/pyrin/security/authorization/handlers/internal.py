# -*- coding: utf-8 -*-
"""
authorization handlers internal module.
"""

import pyrin.security.session.services as session_services

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

    def is_superuser(self):
        """
        gets a value indicating that the current user is superuser.

        :rtype: bool
        """

        user = session_services.get_current_user()
        user_info = session_services.get_current_user_info()
        return self._is_superuser(user, user_info=user_info)
