# -*- coding: utf-8 -*-
"""
security utils cli module.
"""

import pyrin.security.utils.services as security_utils_services

from pyrin.cli.decorators import cli_invoke, cli_group
from pyrin.core.structs import CLI


@cli_group('security_utils')
class SecurityUtilsCLI(CLI):
    """
    security utils cli class.

    this class exposes all security utils cli commands.
    """

    @cli_invoke
    def rsa_key(self, **options):
        """
        generates a pair of public/private rsa keys.

        :keyword int length: key length in bits.

        :returns: tuple[str public_key, str private_key]
        :rtype: tuple[str, str]
        """

        return security_utils_services.generate_rsa_key(**options)

    @cli_invoke
    def bytes(self, **options):
        """
        gets a secure random bytes with given length.

        the result value should not be decoded to string, because
        it's not a safe-string and may cause an error.
        if you want string representation, use `get_hex` or `get_url_safe` methods.

        :keyword int length: length of random bytes to be get.
                             if not provided, `default_secure_random_size`
                             config will be used.

        :rtype: bytes
        """

        return security_utils_services.get_bytes(**options)

    @cli_invoke
    def hex(self, **options):
        """
        gets a secure random hex string with given length.

        :keyword int length: length of random string to be get in bytes.
                             if not provided, `default_secure_random_size`
                             config will be used.

        :rtype: str
        """

        return security_utils_services.get_hex(**options)

    @cli_invoke
    def url_safe(self, **options):
        """
        gets a secure random url-safe string with given length.

        :keyword int length: length of random string to be get in bytes.
                             if not provided, `default_secure_random_size`
                             config will be used.

        :rtype: str
        """

        return security_utils_services.get_url_safe(**options)
