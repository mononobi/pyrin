# -*- coding: utf-8 -*-
"""
authorization services module.
"""

from pyrin.application.services import get_component
from pyrin.security.authorization import AuthorizationPackage


def authorize(user, permission_ids, **options):
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

    return get_component(AuthorizationPackage.COMPONENT_NAME).authorize(user,
                                                                        permission_ids,
                                                                        **options)


def is_authorized(permission_ids, **options):
    """
    gets a value indicating that specified user is authorized for given permissions.

    :param list[object] permission_ids: permission ids to check for authorization.

    :keyword dic user: user identity to be checked for authorization.

    :rtype: bool
    """

    return get_component(AuthorizationPackage.COMPONENT_NAME).is_authorized(
        permission_ids, **options)
