# -*- coding: utf-8 -*-
"""
rs256 token handler module.
"""

import pyrin.configuration.services as config_services

from pyrin.security.token.handlers.base import AsymmetricTokenBase


class RS256Token(AsymmetricTokenBase):
    """
    rs256 token class.
    """

    def __init__(self):
        """
        initializes an instance of RS256Token.
        """

        # we pass the algorithm of token handler as the name of it.
        AsymmetricTokenBase.__init__(self, self._get_algorithm())

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
