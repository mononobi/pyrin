# -*- coding: utf-8 -*-
"""
hs256 token handler module.
"""

import pyrin.configuration.services as config_services
import pyrin.utils.secure_random as secure_random_utils

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

        # we pass the algorithm of token handler as the name of it.
        SymmetricTokenBase.__init__(self, self._get_algorithm(), **options)

    def _get_encoding_key(self, **options):
        """
        gets the signing key for encoding.

        :rtype: str
        """

        return config_services.get('security', 'token', 'hs256_key')

    def _get_algorithm(self):
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

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        return secure_random_utils.get_url_safe()
