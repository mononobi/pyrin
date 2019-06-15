# -*- coding: utf-8 -*-
"""
authorization manager module.
"""

from pyrin.core.context import CoreObject


class AuthorizationManager(CoreObject):
    """
    authorization manager class.
    this class is intended to provide some services needed in pyrin application.
    the top level application must extend this class considering business requirements.
    """

    def authorize(self, user_id, permission_ids):
        """
        authorizes the given user for specified permissions.
        if user does not have each one of specified permissions,
        an error will be raised.

        :param dict user_id: user id to authorize permissions for.
        :param Union[object, list[object]] permission_ids: permission ids to check
                                                           user authorization.

        :raises PermissionDeniedError: permission denied error.
        """

