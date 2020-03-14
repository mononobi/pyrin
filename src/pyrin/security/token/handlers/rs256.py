# -*- coding: utf-8 -*-
"""
rs256 token handler module.
"""

import pyrin.configuration.services as config_services

from pyrin.security.token.decorators import token
from pyrin.security.token.handlers.base import RSTokenBase


@token()
class RS256Token(RSTokenBase):
    """
    rs256 token class.
    """

    def __init__(self, **options):
        """
        initializes an instance of RS256Token.
        """

        super().__init__(**options)

    def _get_encoding_key(self, **options):
        """
        gets the signing key for encoding.

        :rtype: str
        """

        return self._private_key

    def _get_decoding_key(self, **options):
        """
        gets the signing key for decoding.

        :rtype: str
        """

        return self._public_key

    def _get_algorithm(self, **options):
        """
        gets the algorithm for signing the token.

        :rtype: str
        """

        return 'RS256'

    def get_kid(self):
        """
        gets kid value to be used in token header for this handler.
        it must be unique for each handler.

        :rtype: str
        """

        return '8441c8a0-8ec6-4987-ab80-be71c3bef90c'

    def generate_key(self, **options):
        """
        generates a valid public/private key for this handler and returns it.

        :returns: tuple[str public_key, str private_key]
        :rtype: tuple[str, str]
        """

        return super().generate_key(length=2048)

    def _load_keys(self, **options):
        """
        loads public/private keys into this class's relevant attributes.
        """

        self._public_key = config_services.get('security', 'token', 'rs256_public_key')
        self._private_key = config_services.get('security', 'token', 'rs256_private_key')
