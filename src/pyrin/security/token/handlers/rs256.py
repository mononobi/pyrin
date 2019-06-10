# -*- coding: utf-8 -*-
"""
rs256 token handler module.
"""

import pyrin.configuration.services as config_services

from pyrin.security.token.decorators import token
from pyrin.security.token.handlers.base import AsymmetricTokenBase


@token()
class RS256Token(AsymmetricTokenBase):
    """
    rs256 token class.
    """

    def __init__(self, **options):
        """
        initializes an instance of RS256Token.
        """

        AsymmetricTokenBase.__init__(self, **options)

    def _get_encoding_key(self, **options):
        """
        gets the signing key for encoding.

        :rtype: str
        """

        return config_services.get('security', 'token', 'rs256_private_key')

    def _get_decoding_key(self, **options):
        """
        gets the signing key for decoding.

        :rtype: str
        """

        return config_services.get('security', 'token', 'rs256_public_key')

    def _get_algorithm(self):
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
