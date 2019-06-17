# -*- coding: utf-8 -*-
"""
authentication manager module.
"""

import pyrin.security.token.services as token_services

from pyrin.core.context import CoreObject
from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.security.token.exceptions import TokenManagerVerificationFailedException


class AuthenticationManager(CoreObject):
    """
    authentication manager class.
    this class is intended to be an interface for top level application's
    authentication package.
    """

    def authenticate(self, token, **options):
        """
        authenticates given token and pushes the authenticated data into request context.
        if authentication failed, authenticated data will not be pushed into request context.

        :param str token: token to be authenticated.
        """

        payload = {}
        try:
            payload = token_services.get_payload(token, **options)
            self._validate_payload(payload, **options)
            self._push_data(token, payload, **options)

        except TokenManagerVerificationFailedException:
            return

    def _push_data(self, token, payload, **options):
        """
        pushes the specified payload into request context.

        :param dict payload: payload data of authenticated token.
        """
        pass

    def _validate_payload(self, payload, **options):
        """
        validates the given payload.
        an error will be raised if validation fails.

        :param dict payload: payload data to be validated.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()
