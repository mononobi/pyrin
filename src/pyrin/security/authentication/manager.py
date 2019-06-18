# -*- coding: utf-8 -*-
"""
authentication manager module.
"""

import pyrin.security.token.services as token_services
import pyrin.security.session.services as session_services

from pyrin.core.context import CoreObject
from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.security.authentication.exceptions import InvalidComponentCustomKeyError
from pyrin.security.token.exceptions import TokenVerificationError


class AuthenticationManager(CoreObject):
    """
    authentication manager class.
    this class is intended to be an interface for top level application's
    authentication package.
    """

    def authenticate(self, token, **options):
        """
        authenticates given token and pushes the authenticated data into request context.
        if authentication fails, authenticated data will not be pushed into request context.

        :param str token: token to be authenticated.

        :raises AuthenticationFailedError: authentication failed error.
        """

        if token is None:
            return

        try:
            payload = token_services.get_payload(token, **options)
            self._validate_payload(payload, **options)
            self._push_data(payload, **options)

        except TokenVerificationError:
            return

    def _push_data(self, payload, **options):
        """
        pushes the specified inputs into request context.

        :param dict payload: payload data of authenticated token.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()

    def _push_component_custom_key(self, value):
        """
        pushes the provided value as component custom key into request context.

        :param object value: value to be pushed as component custom key.

        :raises InvalidComponentCustomKeyError: invalid component custom key error.
        """

        if value is None:
            raise InvalidComponentCustomKeyError('Component custom key could not be None')

        session_services.add_request_context('component_custom_key', value)

    def _validate_payload(self, payload, **options):
        """
        validates the given payload.
        an error will be raised if validation fails.

        :param dict payload: payload data to be validated.

        :raises CoreNotImplementedError: core not implemented error.
        :raises AuthenticationFailedError: authentication failed error.
        """

        raise CoreNotImplementedError()
