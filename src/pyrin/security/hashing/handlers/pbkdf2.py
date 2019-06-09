# -*- coding: utf-8 -*-
"""
pbkdf2 hashing handler module.
"""

import hashlib

import pyrin.configuration.services as config_services

from pyrin.security.hashing.decorators import hashing
from pyrin.security.hashing.handlers.base import HashingBase
from pyrin.settings.static import APPLICATION_ENCODING
from pyrin.utils import secure_random


@hashing()
class PBKDF2Hashing(HashingBase):
    """
    pbkdf2 hashing class.
    """

    INTERNAL_ALGORITHM = 'sha256'

    def __init__(self, **options):
        """
        initializes an instance of PBKDF2Hashing.
        """

        # we pass the algorithm of hashing handler as the name of it.
        HashingBase.__init__(self, self._get_algorithm(), **options)

    def generate_hash(self, plain_text, **options):
        """
        gets the hash of input plain text and salt.

        :param str plain_text: text to be hashed.

        :keyword bytes salt: salt to append to plain text before hashing.

        :keyword int rounds: rounds to perform for generating hash.
                             if not provided, default value from
                             relevant config will be used.

        :rtype: bytes
        """

        rounds = options.get('rounds', config_services.get('security', 'hashing',
                                                           'pbkdf2_log_rounds'))

        return hashlib.pbkdf2_hmac(self.INTERNAL_ALGORITHM,
                                   plain_text.encode(APPLICATION_ENCODING),
                                   options.get('salt', b''), rounds)

    def generate_salt(self, **options):
        """
        generates a valid salt for this handler and returns it.

        :keyword int length: length of generated salt.
                             some hashing handlers may not accept custom salt length,
                             so this value would be ignored on those handlers.

        :rtype: bytes
        """

        return secure_random.get_bytes(**options)

    def is_match(self, plain_text, hashed_value):
        """
        gets a value indicating that given plain text's
        hash is identical to given hashed value.

        :param str plain_text: text to be hashed.
        :param bytes hashed_value: hashed value to compare with.

        :rtype: bool
        """

        pass

    def _get_algorithm(self):
        """
        gets the hashing algorithm.

        :rtype: str
        """

        return 'PBKDF2'
