# -*- coding: utf-8 -*-
"""
authorization manager module.
"""

import pyrin.application.services as application_services
import pyrin.security.session.services as session_services
import pyrin.security.authentication.services as authentication_services

from pyrin.core.globals import _
from pyrin.core.structs import Manager, Context
from pyrin.utils.custom_print import print_warning
from pyrin.security.authorization import AuthorizationPackage
from pyrin.api.router.handlers.protected import ProtectedRoute
from pyrin.security.authorization.interface import AbstractAuthorizerBase
from pyrin.security.exceptions import AuthorizationFailedError
from pyrin.security.authorization.exceptions import UserNotAuthenticatedError, \
    AuthorizerNotFoundError, InvalidAuthorizerTypeError, DuplicatedAuthorizerError


class AuthorizationManager(Manager):
    """
    authorization manager class.
    """

    package_class = AuthorizationPackage

    def __init__(self):
        """
        initializes an instance of AuthorizationManager.
        """

        super().__init__()

        # a dictionary containing information of registered authorizers.
        # example: dict(str name: AbstractAuthorizerBase instance)
        self._authorizers = Context()

    def authorize(self, user, permissions, **options):
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

        if user is None:
            raise UserNotAuthenticatedError(_('User has not been authenticated.'))

        authorizer_name = options.pop('authorizer', None)
        if authorizer_name is None:
            authorizer_name = authentication_services.get_current_authenticator_name()

        if authorizer_name is None or not self.authorizer_exists(authorizer_name):
            return

        authorizer = self.get_authorizer(authorizer_name)
        try:
            authorizer.authorize(user, permissions, **options)
        except AuthorizationFailedError:
            raise
        except Exception as error:
            raise AuthorizationFailedError(error) from error

    def is_authorized(self, permissions, user=None, **options):
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

        if user is None:
            user = session_services.get_current_user()

        user_info = options.get('user_info')
        if user_info is None:
            user_info = session_services.get_current_user_info()

        try:
            options.update(user_info=user_info)
            self.authorize(user, permissions, **options)
            return True
        except AuthorizationFailedError:
            return False

    def authorizer_exists(self, name):
        """
        gets a value indicating that an authorizer with given name exists.

        :param str name: authorizer name.

        :rtype: bool
        """

        return name in self._authorizers

    def get_authorizer(self, name, **options):
        """
        gets the authorizer with given name.

        :keyword str name: authorizer name.

        :raises AuthorizerNotFoundError: authorizer not found error.

        :rtype: AbstractAuthorizerBase
        """

        if name not in self._authorizers:
            raise AuthorizerNotFoundError('Authorizer [{name}] not found.'
                                          .format(name=name))

        return self._authorizers[name]

    def register_authorizer(self, instance, **options):
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

        if not isinstance(instance, AbstractAuthorizerBase):
            raise InvalidAuthorizerTypeError('Input parameter [{instance}] is '
                                             'not an instance of [{base}].'
                                             .format(instance=instance,
                                                     base=AbstractAuthorizerBase))

        if instance.name in self._authorizers:
            old_instance = self._authorizers.get(instance.name)
            replace = options.get('replace', False)
            if replace is not True:
                raise DuplicatedAuthorizerError('There is another registered '
                                                'authorizer [{old}] with name '
                                                '[{name}] but "replace" option is not '
                                                'set, so authorizer [{instance}] '
                                                'could not be registered.'
                                                .format(old=old_instance,
                                                        name=instance.name,
                                                        instance=instance))

            print_warning('Authorizer [{old_instance}] is going '
                          'to be replaced by [{new_instance}].'
                          .format(old_instance=old_instance,
                                  new_instance=instance))

        self._authorizers[instance.name] = instance

    def validate_authorizers(self):
        """
        validates that all routes with permissions have their authorizers present.

        :raises AuthorizerNotFoundError: authorizer not found error.
        """

        app = application_services.get_current_app()
        for route in app.url_map.get_routes():
            if isinstance(route, ProtectedRoute) and route.permissions and \
                    not self.authorizer_exists(route.authenticator):
                raise AuthorizerNotFoundError('Authorizer with name [{name}] on '
                                              'view function [{endpoint}] does not '
                                              'exist in registered authorizers.'
                                              .format(name=route.authenticator,
                                                      endpoint=route.endpoint))
