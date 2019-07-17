# -*- coding: utf-8 -*-
"""
authorization manager module.
"""

import pyrin.security.services as security_services
import pyrin.security.session.services as session_services

from pyrin.core.globals import _
from pyrin.core.context import CoreObject
from pyrin.security.authorization.exceptions import AuthorizationFailedError, \
    UserNotAuthenticatedError, UserIsNotActiveError


class AuthorizationManager(CoreObject):
    """
    authorization manager class.
    this class is intended to provide some services needed in pyrin application.
    the top level application must extend this class considering business requirements.
    """

    def authorize(self, user, permissions, **options):
        """
        authorizes the given user for specified permissions.
        if user does not have each one of specified permissions,
        an error will be raised.

        :param dict user: user identity to authorize permissions for.

        :param Union[PermissionBase, list[PermissionBase]] permissions: permissions to check
                                                                        for user authorization.

        :raises UserNotAuthenticatedError: user not authenticated error.
        :raises UserIsNotActiveError: user is not active error.
        :raises AuthorizationFailedError: authorization failed error.
        """

        if user is None:
            raise UserNotAuthenticatedError(_('User has not been authenticated.'))

        if not security_services.is_active(user, **options):
            message = _('User [{user}] is not active.')
            raise UserIsNotActiveError(message.format(user=str(user)))

        # we must check whether input permissions object is iterable.
        # if not, we make it manually.
        permissions_collection = permissions
        if not isinstance(permissions, (list, set, tuple)):
            permissions_collection = [permissions]

        permission_ids = [item.get_id() for item in permissions_collection]
        user_permission_ids = security_services.get_user_permission_ids(user, **options)

        if not set(permission_ids) <= set(user_permission_ids):
            message = _('User [{user}] has not required permission(s) [{permission_ids}].')
            raise AuthorizationFailedError(message.format(user=str(user),
                                                          permission_ids=permission_ids))

    def is_authorized(self, permissions, **options):
        """
        gets a value indicating that specified user is authorized for given permissions.

        :param Union[PermissionBase, list[PermissionBase]] permissions: permissions to check
                                                                        for authorization.

        :keyword dict user: user identity to be checked for authorization.
                            if not provided, current user will be used.

        :rtype: bool
        """

        user = options.get('user', None)
        if user is None:
            user = session_services.get_current_user()

        try:
            self.authorize(user, permissions)
            return True
        except AuthorizationFailedError:
            return False
