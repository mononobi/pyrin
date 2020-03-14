# -*- coding: utf-8 -*-
"""
authorization services module.
"""

from pyrin.application.services import get_component
from pyrin.security.authorization import AuthorizationPackage


def authorize(user, permissions, **options):
    """
    authorizes the given user for specified permissions.
    if user does not have each one of specified permissions,
    an error will be raised.

    :param user: user identity to authorize permissions for.

    :param PermissionBase | list[PermissionBase] permissions: permissions to check
                                                              for user authorization.

    :raises UserNotAuthenticatedError: user not authenticated error.
    :raises AuthorizationFailedError: authorization failed error.
    """

    return get_component(AuthorizationPackage.COMPONENT_NAME).authorize(user,
                                                                        permissions,
                                                                        **options)


def is_authorized(permissions, user=None, **options):
    """
    gets a value indicating that specified user is authorized for given permissions.

    :param PermissionBase | list[PermissionBase] permissions: permissions to check
                                                              for authorization.

    :param user: user identity to be checked for authorization.
                 if not provided, current user will be used.

    :rtype: bool
    """

    return get_component(AuthorizationPackage.COMPONENT_NAME).is_authorized(permissions,
                                                                            user,
                                                                            **options)
