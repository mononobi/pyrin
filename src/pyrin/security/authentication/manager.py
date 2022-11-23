# -*- coding: utf-8 -*-
"""
authentication manager module.
"""

import pyrin.validator.services as validator_services
import pyrin.application.services as application_services
import pyrin.security.session.services as session_services
import pyrin.configuration.services as config_services
import pyrin.utils.dictionary as dict_utils

from pyrin.core.structs import Manager, Context
from pyrin.utils.custom_print import print_warning
from pyrin.api.router.handlers.protected import ProtectedRoute
from pyrin.security.authentication import AuthenticationPackage
from pyrin.security.authentication.interface import AbstractAuthenticatorBase
from pyrin.security.exceptions import AuthenticationFailedError
from pyrin.security.authentication.exceptions import InvalidAuthenticatorTypeError, \
    DuplicatedAuthenticatorError, AuthenticatorNotFoundError


class AuthenticationManager(Manager):
    """
    authentication manager class.
    """

    package_class = AuthenticationPackage

    def __init__(self):
        """
        initializes an instance of AuthenticationManager.
        """

        super().__init__()

        # a dictionary containing information of registered authenticators.
        # example: dict(str name: AbstractAuthenticatorBase instance)
        self._authenticators = Context()
        self._default_authenticator = config_services.get_active('authentication',
                                                                 'default_authenticator')

        # a dictionary containing all rule based authenticators in the form of:
        # dict(str url_rule: str name)
        # for example:
        # {'/api/customers': 'customer',
        #  '/api/sellers': 'seller',
        #  '/api': 'api'}
        self._rule_based_authenticators = self._load_rule_based_authenticators()

    def _load_rule_based_authenticators(self):
        """
        loads rule based authenticators from `authentication` config store.

        we sort rule based authenticators by length of their name in descending order.
        this is required to be able to detect the closest match to each url rule.

        :rtype: dict
        """

        authenticators = config_services.get_active('authentication',
                                                    'rule_based_authenticators')
        return dict_utils.sort_by_key_length(authenticators, reverse=True)

    def get_relevant_authenticator_name(self, url):
        """
        gets the relevant authenticator name for given url rule.

        it looks for relevant authenticator in the following order:

        1. looking for it in rule based authenticators.
        2. getting default authenticator for it.

        it may return None if no relevant authenticator could be found.

        :param str url: url rule to find a relevant authenticator for it.

        :rtype: str
        """

        authenticator = self.get_rule_based_authenticator_name(url)
        if not authenticator:
            authenticator = self._default_authenticator

        return authenticator

    def get_current_authenticator_name(self):
        """
        gets the authenticator name for current request from its matched url rule.

        it may return None if the current request does not match any url rule.
        it also returns None for routes which have `authenticated=False` in their
        definition.

        :rtype: str
        """

        current_request = session_services.get_current_request()
        if current_request.url_rule and isinstance(current_request.url_rule, ProtectedRoute):
            return current_request.url_rule.authenticator

        return None

    def get_current_authenticator(self):
        """
        gets the authenticator for current request from its matched url rule.

        it may return None if the current request does not match any url rule.
        it also returns None for routes which have `authenticated=False` in their
        definition.

        :rtype: AbstractAuthenticatorBase
        """

        name = self.get_current_authenticator_name()
        if name:
            return self.get_authenticator(name)

        return None

    def get_rule_based_authenticator_name(self, url):
        """
        gets the relevant authenticator name to the given url rule.

        it may return None if no matching rule is found.

        :param str url: url to get its matching authenticator name.

        :rtype: str
        """

        if url[-1] != '/':
            url = f'{url}/'

        for rule, name in self._rule_based_authenticators.items():
            if url.startswith(rule):
                return name

        return None

    def authenticator_exists(self, name):
        """
        gets a value indicating that an authenticator with given name exists.

        :param str name: authenticator name.

        :rtype: bool
        """

        return name in self._authenticators

    def get_authenticator(self, name, **options):
        """
        gets the authenticator with given name.

        :keyword str name: authenticator name.

        :raises AuthenticatorNotFoundError: authenticator not found error.

        :rtype: AbstractAuthenticatorBase
        """

        if name not in self._authenticators:
            raise AuthenticatorNotFoundError('Authenticator [{name}] not found.'
                                             .format(name=name))

        return self._authenticators[name]

    def register_authenticator(self, instance, **options):
        """
        registers a new authenticator or replaces the existing one.

        if `replace=True` is provided. otherwise, it raises an error
        on adding an authenticator which is already registered.

        :param AbstractAuthenticatorBase instance: authenticator to be registered.
                                                   it must be an instance of
                                                   AbstractAuthenticatorBase.

        :keyword bool replace: specifies that if there is another registered
                               authenticator with the same name, replace it with
                               the new one, otherwise raise an error.
                               defaults to False.

        :raises InvalidAuthenticatorTypeError: invalid authenticator type error.
        :raises DuplicatedAuthenticatorError: duplicated authenticator error.
        """

        if not isinstance(instance, AbstractAuthenticatorBase):
            raise InvalidAuthenticatorTypeError('Input parameter [{instance}] is '
                                                'not an instance of [{base}].'
                                                .format(instance=instance,
                                                        base=AbstractAuthenticatorBase))

        if instance.name in self._authenticators:
            old_instance = self._authenticators.get(instance.name)
            replace = options.get('replace', False)
            if replace is not True:
                raise DuplicatedAuthenticatorError('There is another registered '
                                                   'authenticator [{old}] with name '
                                                   '[{name}] but "replace" option is not '
                                                   'set, so authenticator [{instance}] '
                                                   'could not be registered.'
                                                   .format(old=old_instance,
                                                           name=instance.name,
                                                           instance=instance))

            print_warning('Authenticator [{old_instance}] is going '
                          'to be replaced by [{new_instance}].'
                          .format(old_instance=old_instance,
                                  new_instance=instance))

        self._authenticators[instance.name] = instance

    def validate_authenticators(self):
        """
        validates that all protected routes authenticators are present.

        :raises AuthenticatorNotFoundError: authenticator not found error.
        """

        app = application_services.get_current_app()
        for route in app.url_map.get_routes():
            if isinstance(route, ProtectedRoute) and \
                    not self.authenticator_exists(route.authenticator):
                raise AuthenticatorNotFoundError('Authenticator with name [{name}] on '
                                                 'view function [{endpoint}] does not '
                                                 'exist in registered authenticators.'
                                                 .format(name=route.authenticator,
                                                         endpoint=route.endpoint))

    def authenticate(self, request, **options):
        """
        authenticates given request and pushes the authenticated data into current request.

        if authentication fails, authenticated data will not be pushed into current request.

        :param CoreRequest request: request to be authenticated.

        :keyword str authenticator: authenticator name to be used. if not
                                    provided, current request authenticator
                                    will be used. if current request does
                                    not have an authenticator, nothing will
                                    be done.

        :raises AuthenticationFailedError: authentication failed error.
        """

        authenticator_name = options.get('authenticator')
        if not authenticator_name:
            authenticator_name = self.get_current_authenticator_name()

        if authenticator_name:
            authenticator = self.get_authenticator(authenticator_name)
            try:
                authenticator.authenticate(request, **options)
            except AuthenticationFailedError:
                raise
            except Exception as error:
                raise AuthenticationFailedError(error) from error

    def login(self, username, password, authenticator, **options):
        """
        logs in a user with given info using provided authenticator.

        it may return the required credentials if they must be returned to client.

        :param str username: username.
        :param str password: password.
        :param str authenticator: authenticator name to be used.

        :raises ValidationError: validation error.
        :raises AuthenticatorNotFoundError: authenticator not found error.

        :returns: required credentials.
        """

        data = validator_services.validate('authentication',
                                           username=username,
                                           password=password)

        authenticator = self.get_authenticator(authenticator, **options)
        return authenticator.login(data.username, data.password, **options)

    def logout(self, authenticator, **options):
        """
        logouts the current user and clears its relevant credentials.

        :param str authenticator: authenticator name to be used.

        :raises AuthenticatorNotFoundError: authenticator not found error.
        """

        authenticator = self.get_authenticator(authenticator, **options)
        return authenticator.logout(**options)
