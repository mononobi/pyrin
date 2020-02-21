# -*- coding: utf-8 -*-
"""
hs256 token handler module.
"""

import pyrin.configuration.services as config_services
import pyrin.security.utils.services as security_utils_services

from pyrin.security.token.decorators import token
from pyrin.security.token.handlers.base import SymmetricTokenBase


@token()
class HS256Token(SymmetricTokenBase):
    """
    hs256 token class.
    """

    def __init__(self, **options):
        """
        initializes an instance of HS256Token.
        """

        super().__init__(**options)

    def _get_encoding_key(self, **options):
        """
        gets the signing key for encoding.

        :rtype: str
        """

        return config_services.get('security', 'token', 'hs256_key')

    def _get_algorithm(self, **options):
        """
        gets the algorithm for signing the token.

        :rtype: str
        """

        return 'HS256'

    def generate_key(self, **options):
        """
        generates a valid key for this handler and returns it.

        :keyword int length: the length of generated key in bytes.
                             note that some token handlers may not accept custom
                             key length so this value would be ignored on those handlers.

        :rtype: str
        """

        key_length = options.get('length', None)
        if key_length is None:
            key_length = config_services.get('security', 'token', 'hs256_key_length')

        return security_utils_services.get_url_safe(length=key_length)

    def get_kid(self):
        """
        gets kid value to be used in token header for this handler.
        it must be unique for each handler.

        :rtype: str
        """

        return '494d8b2d-ae91-442d-86eb-9fd020fe3518'
