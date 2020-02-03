# -*- coding: utf-8 -*-
"""
authorization manager module.
"""

import pyrin.security.services as security_services
import pyrin.security.users.services as user_services
import pyrin.security.session.services as session_services

from pyrin.core.globals import _, LIST_TYPES
from pyrin.core.context import Manager
from pyrin.security.authorization.exceptions import AuthorizationFailedError, \
    UserNotAuthenticatedError, UserIsNotActiveError


class AuthorizationManager(Manager):
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

        :param user: user identity to authorize permissions for.

        :param Union[PermissionBase, list[PermissionBase]] permissions: permissions to check
                                                                        for user authorization.

        :raises UserNotAuthenticatedError: user not authenticated error.
        :raises UserIsNotActiveError: user is not active error.
        :raises AuthorizationFailedError: authorization failed error.
        """

        if user is None:
            raise UserNotAuthenticatedError(_('User has not been authenticated.'))

        if not user_services.is_active(user, **options):
            message = _('User [{user}] is not active.')
            raise UserIsNotActiveError(message.format(user=str(user)))

        # we must check whether input permissions object is iterable.
        # if not, we make it manually.
        required_permissions = permissions
        if not isinstance(permissions, LIST_TYPES):
            required_permissions = [permissions]

        if security_services.has_permission(user, required_permissions, **options) is not True:
            message = _('User [{user}] does not have required permission(s) {permissions}.')
            raise AuthorizationFailedError(message.format(user=str(user),
                                                          permissions=str(required_permissions)))

    def is_authorized(self, permissions, user=None, **options):
        """
        gets a value indicating that specified user is authorized for given permissions.

        :param Union[PermissionBase, list[PermissionBase]] permissions: permissions to check
                                                                        for authorization.

        :param user: user identity to be checked for authorization.
                     if not provided, current user will be used.

        :rtype: bool
        """

        if user is None:
            user = session_services.get_current_user()

        try:
            self.authorize(user, permissions)
            return True
        except AuthorizationFailedError:
            return False
