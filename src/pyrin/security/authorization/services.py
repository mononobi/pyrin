# -*- coding: utf-8 -*-
"""
authorization services module.
"""

import pyrin.configuration.services as config_services

from pyrin.application.services import get_component
from pyrin.caching.decorators import custom_cached
from pyrin.security.authorization import AuthorizationPackage


cache_name = config_services.get('security', 'authorization', 'cache_name')
cache_expire = config_services.get('security', 'authorization', 'cache_expire')
if cache_name is not None:
    @custom_cached(cache_name, expire=cache_expire, consider_user=True, refreshable=False)
    def authorize(user, permissions, **options):
        """
        authorizes the given user for specified permissions.

        if user does not have each one of the specified
        permissions, an error will be raised.

        :param user: user identity to authorize permissions for.

        :param PermissionBase | list[PermissionBase] permissions: permissions to check
                                                                  for user authorization.

        :keyword str authorizer: authorizer name to be used.
                                 if not provided, current request authenticator will
                                 be used. if current request does not have an
                                 authenticator, it will consider it as authorized.

        :keyword dict user_info: user info to be used for authorization.

        :raises UserNotAuthenticatedError: user not authenticated error.
        :raises AuthorizationFailedError: authorization failed error.
        """

        return get_component(AuthorizationPackage.COMPONENT_NAME).authorize(user, permissions,
                                                                            **options)


    @custom_cached(cache_name, expire=cache_expire, consider_user=True, refreshable=False)
    def is_authorized(permissions, user=None, **options):
        """
        gets a value indicating that specified user is authorized for given permissions.

        :param PermissionBase | list[PermissionBase] permissions: permissions to check
                                                                  for authorization.

        :param user: user identity to be checked for authorization.
                     if not provided, current user will be used.

        :keyword str authorizer: authorizer name to be used.
                                 if not provided, current request authenticator will
                                 be used. if current request does not have an
                                 authenticator, it will return True as authorized.

        :keyword dict user_info: user info to be used for authorization.
                                 if not provided, current user info will be used.

        :rtype: bool
        """

        return get_component(AuthorizationPackage.COMPONENT_NAME).is_authorized(permissions, user,
                                                                                **options)

else:
    def authorize(user, permissions, **options):
        """
        authorizes the given user for specified permissions.

        if user does not have each one of the specified
        permissions, an error will be raised.

        :param user: user identity to authorize permissions for.

        :param PermissionBase | list[PermissionBase] permissions: permissions to check
                                                                  for user authorization.

        :keyword str authorizer: authorizer name to be used.
                                 if not provided, current request authenticator will
                                 be used. if current request does not have an
                                 authenticator, it will consider it as authorized.

        :keyword dict user_info: user info to be used for authorization.

        :raises UserNotAuthenticatedError: user not authenticated error.
        :raises AuthorizationFailedError: authorization failed error.
        """

        return get_component(AuthorizationPackage.COMPONENT_NAME).authorize(user, permissions,
                                                                            **options)


    def is_authorized(permissions, user=None, **options):
        """
        gets a value indicating that specified user is authorized for given permissions.

        :param PermissionBase | list[PermissionBase] permissions: permissions to check
                                                                  for authorization.

        :param user: user identity to be checked for authorization.
                     if not provided, current user will be used.

        :keyword str authorizer: authorizer name to be used.
                                 if not provided, current request authenticator will
                                 be used. if current request does not have an
                                 authenticator, it will return True as authorized.

        :keyword dict user_info: user info to be used for authorization.
                                 if not provided, current user info will be used.

        :rtype: bool
        """

        return get_component(AuthorizationPackage.COMPONENT_NAME).is_authorized(permissions, user,
                                                                                **options)


def authorizer_exists(name):
    """
    gets a value indicating that an authorizer with given name exists.

    :param str name: authorizer name.

    :rtype: bool
    """

    return get_component(AuthorizationPackage.COMPONENT_NAME).authorizer_exists(name)


def get_authorizer(name, **options):
    """
    gets the authorizer with given name.

    :keyword str name: authorizer name.

    :raises AuthorizerNotFoundError: authorizer not found error.

    :rtype: AbstractAuthorizerBase
    """

    return get_component(AuthorizationPackage.COMPONENT_NAME).get_authorizer(name, **options)


def register_authorizer(instance, **options):
    """
    registers a new authorizer or replaces the existing one.

    if `replace=True` is provided. otherwise, it raises an error
    on adding an authorizer which is already registered.

    :param AbstractAuthorizerBase instance: authorizer to be registered.
                                            it must be an instance of
                                            AbstractAuthorizerBase.

    :keyword bool replace: specifies that if there is another registered
                           authorizer with the same name, replace it with
                           the new one, otherwise raise an error.
                           defaults to False.

    :raises InvalidAuthorizerTypeError: invalid authorizer type error.
    :raises DuplicatedAuthorizerError: duplicated authorizer error.
    """

    return get_component(AuthorizationPackage.COMPONENT_NAME).register_authorizer(instance,
                                                                                  **options)


def validate_authorizers():
    """
    validates that all routes with permissions have their authorizers present.

    :raises AuthorizerNotFoundError: authorizer not found error.
    """

    return get_component(AuthorizationPackage.COMPONENT_NAME).validate_authorizers()
