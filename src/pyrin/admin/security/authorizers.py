# -*- coding: utf-8 -*-
"""
admin security authorizers module.
"""

from pyrin.core.globals import _
from pyrin.security.authorization.decorators import authorizer
from pyrin.admin.security.exceptions import AdminAccessNotAllowedError
from pyrin.security.authorization.handlers.internal import InternalAuthorizer


@authorizer()
class AdminAuthorizer(InternalAuthorizer):
    """
    admin authorizer class.
    """

    _name = 'admin'

    def _authorize_access(self, user, **options):
        """
        authorizes the given internal user for admin access.

        :param int user: internal user id to be checked if it is authorized.

        :keyword dict user_info: internal user info to be used to check for user.

        :raises AdminAccessNotAllowedError: admin access not allowed error.
        """

        user_info = options.get('user_info', {})
        if not user_info.get('admin_access'):
            raise AdminAccessNotAllowedError(_('You are not allowed to access the admin panel. '
                                               'If you think that this is a mistake, please '
                                               'contact the support team.'))
