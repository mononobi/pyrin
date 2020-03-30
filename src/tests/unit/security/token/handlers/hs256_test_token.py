# -*- coding: utf-8 -*-
"""
hs256 test token handler module.
"""

from pyrin.security.token.handlers.hs256 import HS256Token


class HS256TestToken(HS256Token):
    """
    hs256 test token class.
    """

    def _get_algorithm(self, **options):
        """
        gets the algorithm for signing the token.

        :rtype: str
        """

        return 'TEST'

    def get_kid(self):
        """
        gets kid value to be used in token header for this handler.
        it must be unique for each handler.

        :rtype: str
        """

        return 'f825ccd5-9b4a-476f-ae12-c1c1ea99e6b2'
