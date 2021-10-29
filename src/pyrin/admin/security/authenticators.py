# -*- coding: utf-8 -*-
"""
admin security authenticators module.
"""

from pyrin.security.enumerations import InternalAuthenticatorEnum
from pyrin.security.authentication.decorators import authenticator
from pyrin.security.authentication.handlers.internal import InternalTokenAuthenticator


@authenticator()
class AdminTokenAuthenticator(InternalTokenAuthenticator):
    """
    internal token authenticator class.
    """

    REFRESH_TOKEN_HOLDER = 'Admin-Refresh-Auth'
    _name = InternalAuthenticatorEnum.ADMIN

    def _get_extra_user_info(self, user, **options):
        """
        gets extra user info for given internal user if required.

        :param ROW_RESULT user: internal user to get its extra info.

        :rtype: dict
        """

        return dict(admin_access=user.admin_access)
