# -*- coding: utf-8 -*-
"""
authorization manager module.
"""

import pyrin.security.services as security_services
import pyrin.security.session.services as session_services

from pyrin.core.context import CoreObject
from pyrin.security.authorization.exceptions import AuthorizationFailedError, \
    UserNotAuthenticatedError, AuthorizationManagerBusinessException


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

        :raises UserNotAuthenticatedError: user not authenticated error.
        :raises AuthorizationFailedError: authorization failed error.
        """

        if user is None:
            raise UserNotAuthenticatedError('User has not been authenticated.')

        # we must check whether input permission_ids is iterable.
        # if not, we make it manually.
        permission_ids_collection = permission_ids
        if not isinstance(permission_ids, (list, set, tuple)):
            permission_ids_collection = [permission_ids]

        user_permission_ids = security_services.get_user_permission_ids(user, **options)

        if not set(permission_ids_collection) <= set(user_permission_ids):
            message = 'User [{user}] has not required permission(s) [{permission_ids}].'
            raise AuthorizationFailedError(message.format(user=str(user),
                                                          permission_ids=permission_ids))

    def is_authorized(self, permission_ids, **options):
        """
        gets a value indicating that specified user is authorized for given permissions.

        :param list[object] permission_ids: permission ids to check for authorization.

        :keyword dic user: user identity to be checked for authorization.

        :rtype: bool
        """

        user = options.get('user', None)
        if user is None:
            user = session_services.get_current_user()

        try:
            self.authorize(user, permission_ids, **options)
            return True
        except AuthorizationManagerBusinessException:
            return False
