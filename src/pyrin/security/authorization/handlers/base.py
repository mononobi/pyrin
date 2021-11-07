# -*- coding: utf-8 -*-
"""
authorization handlers base module.
"""

from abc import abstractmethod

import pyrin.security.session.services as session_services
import pyrin.utils.misc as misc_utils

from pyrin.core.globals import _, _n
from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.security.authorization.interface import AbstractAuthorizerBase
from pyrin.security.exceptions import UserIsNotActiveError
from pyrin.security.authorization.handlers.exceptions import AuthorizerNameIsRequiredError
from pyrin.security.authorization.exceptions import UserNotAuthenticatedError, \
    PermissionDeniedError


class AuthorizerBase(AbstractAuthorizerBase):
    """
    authorizer base class.

    all application authorizers must be subclassed from this.
    """

    # each subclass must set an authorizer name in this attribute.
    _name = None

    def __init__(self, *args, **options):
        """
        initializes and instance of AuthorizerBase.

        :raises AuthorizerNameIsRequiredError: authorizer name is required error.
        """

        super().__init__()

        if not self._name or self._name.isspace():
            raise AuthorizerNameIsRequiredError('Authorizer [{instance}] does not '
                                                'have a name.'.format(instance=self))

    def _authorize_access(self, user, **options):
        """
        authorizes the given user for custom accesses.

        this method could be overridden in subclasses if required.
        it must raise an error if authorization failed.

        :param user: user identity to be checked if it is authorized.

        :keyword dict user_info: user info to be used to check for user.

        :raises AuthorizationFailedError: authorization failed error.
        """
        pass

    def _is_superuser(self, user, **options):
        """
        gets a value indicating that given user is superuser.

        this method could be overridden in subclasses to provide actual
        implementation for checking that a user is superuser.
        otherwise this method will always return False.

        :param user: user identity to be checked if it is superuser.

        :keyword dict user_info: user info to be used to check for user.

        :rtype: bool
        """

        return False

    def _is_active(self, user, **options):
        """
        gets a value indicating that the given user is active.

        this method could be overridden in subclasses to provide actual
        implementation for checking that a user is active.
        otherwise this method will always return True.

        :param user: user identity to be checked if it is active.

        :keyword dict user_info: user info to be used to check for user.

        :rtype: bool
        """

        return True

    def _authorize_permissions(self, user, permissions, **options):
        """
        authorizes the given user for specified permissions.

        if user does not have each one of the specified
        permissions, an error will be raised.

        :param user: user identity to be checked if it is authorized.

        :param PermissionBase | list[PermissionBase] permissions: permissions to check
                                                                  for user authorization.

        :keyword dict user_info: user info to be used for authorization.

        :raises PermissionDeniedError: permission denied error.
        """

        permissions = misc_utils.make_iterable(permissions, tuple)
        if len(permissions) > 0:
            if self._has_permission(user, permissions, **options) is not True:
                message = _n('You do not have the required permission {permissions}',
                             'You do not have the required permissions {permissions}',
                             len(permissions))
                raise PermissionDeniedError(message.format(permissions=list(permissions)))

    def authorize(self, user, permissions, **options):
        """
        authorizes the given user for specified permissions.

        if user does not have each one of the specified
        permissions, an error will be raised.

        :param user: user identity to authorize permissions for.

        :param PermissionBase | list[PermissionBase] permissions: permissions to check
                                                                  for user authorization.

        :keyword dict user_info: user info to be used for authorization.

        :raises UserNotAuthenticatedError: user not authenticated error.
        :raises UserIsNotActiveError: user is not active error.
        :raises AuthorizationFailedError: authorization failed error.
        :raises PermissionDeniedError: permission denied error.
        """

        if user is None:
            raise UserNotAuthenticatedError(_('User has not been authenticated.'))

        if self._is_active(user, **options) is not True:
            raise UserIsNotActiveError(_('Your user is not active. If you think that this '
                                         'is a mistake, please contact the support team.'))

        if self._is_superuser(user, **options) is not True:
            self._authorize_access(user, **options)
            if permissions:
                self._authorize_permissions(user, permissions, **options)

    def is_superuser(self):
        """
        gets a value indicating that the current user is superuser.

        if you want to provide the actual implementation for checking that a
        user is superuser, you should implement the `_is_superuser` method.
        otherwise this method will always return False.

        :rtype: bool
        """

        user = session_services.get_current_user()
        user_info = session_services.get_current_user_info()
        return self._is_superuser(user, user_info=user_info)

    @abstractmethod
    def _has_permission(self, user, permissions, **options):
        """
        gets a value indicating that given user has the requested permissions.

        this method must be overridden in subclasses to perform a check on permissions.

        :param user: user identity to authorize permissions for.
        :param tuple[PermissionBase] permissions: permissions to check for user authorization.

        :keyword dict user_info: user info to be used for authorization.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: bool
        """

        raise CoreNotImplementedError()

    @property
    def name(self):
        """
        gets the name of this authenticator.

        :rtype: str
        """

        return self._name
