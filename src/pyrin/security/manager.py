# -*- coding: utf-8 -*-
"""
security manager module.
"""

import pyrin.security.encryption.services as encryption_services
import pyrin.security.hashing.services as hashing_services

from pyrin.core.context import CoreObject
from pyrin.security.exceptions import InvalidPasswordError


class SecurityManager(CoreObject):
    """
    security manager class.
    this class is intended to be an interface for top level application's security
    package, so most methods of this class will raise CoreNotImplementedError.
    """

    def get_password_hash(self, password, **options):
        """
        gets the given password's hash.

        :param str password: password to get it's hash.

        :keyword bool is_encrypted: specifies that given password is encrypted.

        :keyword str encryption_handler: specifies which encryption handler should be used.
                                         if not provided, `default_encryption_handler` key
                                         from security configs will be used.

        :keyword str hashing_handler: specifies which hashing handler should be used.
                                      if not provided, `default_hashing_handler` key
                                      from security configs will be used.

        :rtype: bytes
        """

        if password is None or len(password) == 0:
            raise InvalidPasswordError('Input password is invalid.')

        decrypted_password = password
        is_encrypted = options.get('is_encrypted', False)
        if is_encrypted is True:
            decrypted_password = \
                encryption_services.decrypt(password,
                                            handler_name=options.get('encryption_handler'),
                                            **options)

        hashed_password = \
            hashing_services.generate_hash(decrypted_password,
                                           handler_name=options.get('hashing_handler'),
                                           **options)

        return hashed_password
