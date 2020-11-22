# -*- coding: utf-8 -*-
"""
authentication manager module.
"""

from abc import abstractmethod

import pyrin.security.token.services as token_services
import pyrin.security.session.services as session_services

from pyrin.core.globals import _
from pyrin.core.structs import Manager
from pyrin.security.authentication import AuthenticationPackage
from pyrin.security.enumerations import TokenTypeEnum
from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.security.authentication.exceptions import AuthenticationFailedError, \
    AccessTokenRequiredError, InvalidPayloadDataError


class AuthenticationManager(Manager):
    """
    authentication manager class.

    this class is intended to be an interface for top level
    application's authentication package.
    """

    package_class = AuthenticationPackage

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
