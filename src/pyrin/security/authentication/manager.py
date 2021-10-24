# -*- coding: utf-8 -*-
"""
authentication manager module.
"""

from abc import abstractmethod
from collections import OrderedDict

import pyrin.application.services as application_services
import pyrin.security.token.services as token_services
import pyrin.security.session.services as session_services
import pyrin.configuration.services as config_services
import pyrin.utils.dictionary as dict_utils

from pyrin.core.globals import _
from pyrin.core.structs import Manager
from pyrin.utils.custom_print import print_warning
from pyrin.security.enumerations import TokenTypeEnum
from pyrin.api.router.handlers.protected import ProtectedRoute
from pyrin.security.authentication import AuthenticationPackage
from pyrin.security.authentication.interface import AbstractAuthenticatorBase
from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.security.authentication.exceptions import AuthenticationFailedError, \
    AccessTokenRequiredError, InvalidPayloadDataError, InvalidAuthenticatorTypeError, \
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
        self._authenticators = OrderedDict()
        self._default_authenticator = config_services.get_active('authentication',
                                                                 'default_authenticator')

        self._rule_based_authenticators = self._load_rule_based_authenticators()

    def _load_rule_based_authenticators(self):
        """
        loads rule based authenticators from `authentication` config store.

        we sort rule based authenticators by length of their name in descending order.
        this is required to be able to detect closest match to each url rule.

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

    def authenticate(self, client_request, **options):
        """
        authenticates given request and pushes the authenticated data into request context.

        if authentication fails, authenticated data will not be pushed into request context.

        :param CoreRequest client_request: request to be authenticated.

        :raises AuthenticationFailedError: authentication failed error.
        :raises InvalidPayloadDataError: invalid payload data error.
        :raises AccessTokenRequiredError: access token required error.
        """

        token = self._extract_token(client_request)
        if token in (None, ''):
            return

        self._authenticate(token, **options)

    def _authenticate(self, token, **options):
        """
        authenticates given token and pushes the authenticated data into request context.

        if authentication fails, authenticated data will not be pushed into request context.

        :param str token: token to be authenticated.

        :raises AuthenticationFailedError: authentication failed error.
        :raises InvalidPayloadDataError: invalid payload data error.
        :raises AccessTokenRequiredError: access token required error.
        """

        try:
            payload = token_services.get_payload(token, **options)
            header = token_services.get_unverified_header(token, **options)
            self._validate(header, payload, **options)
            self._push_data(header, payload, **options)

        except AuthenticationFailedError:
            raise
        except Exception as error:
            raise AuthenticationFailedError(error) from error

    def _extract_token(self, client_request):
        """
        extracts token from request header if available.

        :param CoreRequest client_request: request object.

        :returns: token
        :rtype: str
        """

        return client_request.authorization

    def _push_data(self, header, payload, **options):
        """
        pushes the required data into current request from input values.

        :param dict header: token header data.
        :param dict payload: payload data of authenticated token.
        """

        session_services.add_request_context('token_header', header)
        session_services.add_request_context('token_payload', payload)

        self._push_custom_data(header, payload, **options)

    @abstractmethod
    def _push_custom_data(self, header, payload, **options):
        """
        pushes the custom data into current request from input values.

        :param dict header: token header data.
        :param dict payload: payload data of authenticated token.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    def _push_component_custom_key(self, value):
        """
        pushes the provided value as component custom key into request.

        this method could be called in subclasses of this class in
        `_push_custom_data()` method if needed.

        :param object value: value to be pushed as component custom key.

        :raises InvalidComponentCustomKeyError: invalid component custom key error.
        """

        session_services.set_component_custom_key(value)

    def _validate(self, header, payload, **options):
        """
        validates the given inputs.

        an error will be raised if validation fails.

        :param dict header: token header data.
        :param dict payload: payload data to be validated.

        :raises InvalidPayloadDataError: invalid payload data error.
        :raises AccessTokenRequiredError: access token required error.
        """

        if payload is None:
            raise InvalidPayloadDataError(_('Payload data could not be None.'))

        token_type = payload.get('type', None)
        if token_type != TokenTypeEnum.ACCESS:
            raise AccessTokenRequiredError(_('Access token is required for authentication.'))

        self._validate_custom(header, payload, **options)

    @abstractmethod
    def _validate_custom(self, header, payload, **options):
        """
        validates the given inputs for custom attributes.

        an error will be raised if validation fails.

        :param dict header: token header data.
        :param dict payload: payload data to be validated.

        :raises CoreNotImplementedError: core not implemented error.
        :raises AuthenticationFailedError: authentication failed error.
        """

        raise CoreNotImplementedError()
