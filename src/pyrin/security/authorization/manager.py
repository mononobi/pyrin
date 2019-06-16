# -*- coding: utf-8 -*-
"""
authorization manager module.
"""

import pyrin.security.services as security_services

from pyrin.core.context import CoreObject
from pyrin.security.authorization.exceptions import AuthorizationFailedError


class AuthorizationManager(CoreObject):
    """
    authorization manager class.
    this class is intended to provide some services needed in pyrin application.
    the top level application must extend this class considering business requirements.
    """

    def authorize(self, user, permission_ids, **options):
        """
        authorizes the given user for specified permissions.
        if user does not have each one of specified permissions,
        an error will be raised.

        :param dict user: user identity to authorize permissions for.

        :param Union[object, list[object]] permission_ids: permission ids to check
                                                           user authorization.

        :raises AuthorizationFailedError: authorization failed error.
        """

        # we must check if input permission_ids is not iterable, make it manually.
        permission_ids_collection = permission_ids
        if not isinstance(permission_ids, (list, set, tuple)):
            permission_ids_collection = [permission_ids]

        user_permission_ids = security_services.get_user_permission_ids(user, **options)

        if not set(permission_ids_collection) <= set(user_permission_ids):
            message = 'User [{user}] has not required permission(s) [{permission_ids}].'
            raise AuthorizationFailedError(message.format(user=str(user),
                                                          permission_ids=permission_ids))
