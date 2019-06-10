# -*- coding: utf-8 -*-
"""
bcrypt hashing handler module.
"""

import bcrypt

import pyrin.configuration.services as config_services

from pyrin.security.hashing.decorators import hashing
from pyrin.security.hashing.handlers.base import HashingBase
from pyrin.security.hashing.handlers.exceptions import BcryptMaxSizeLimitError
from pyrin.settings.static import APPLICATION_ENCODING


@hashing()
class BcryptHashing(HashingBase):
    """
    bcrypt hashing class.
    """

    # bcrypt hashing has a max size value that could be hashed, original
    # implementation truncates the input string to satisfy max size limit.
    # though the max size differs on different bcrypt implementations, so
    # we consider 50 bytes as a safe max size for all implementations.
    # 50 bytes is equivalent to 50 chars in ascii encoding, not unicode.
    MAX_SIZE = 50

    def __init__(self, **options):
        """
        initializes an instance of BcryptHashing.
        """

        # we pass the algorithm of hashing handler as the name of it.
        HashingBase.__init__(self, self._get_algorithm(), **options)

    def generate_hash(self, text, **options):
        """
        gets the hash of input text using a random or specified salt.
        the result is in the form of `$prefix$rounds$salt-text_hash`.

        :param str text: text to be hashed.

        :keyword bytes salt: salt to be used for hashing.
                             if not provided, a random salt will be generated.

        :keyword str prefix: prefix to be used for hashing.

        :keyword int rounds: rounds to perform for generating hash.
                             if not provided, default value from
                             relevant config will be used.

        :raises BcryptMaxSizeLimitError: bcrypt max size limit error.

        :rtype: bytes
        """

        text_bytes = self._digest_inputs(text, **options)

        salt = options.get('salt', None)
        if salt is None:
            salt = self._generate_salt(**options)

        return bcrypt.hashpw(text_bytes, salt)

    def _generate_salt(self, **options):
        """
        generates a valid salt for this handler and returns it.

        :keyword str prefix: prefix to be used for hashing.

        :keyword int rounds: rounds to perform for generating hash.
                             if not provided, default value from
                             relevant config will be used.

        :rtype: bytes
        """

        rounds = options.get('rounds', config_services.get('security', 'hashing',
                                                           'bcrypt_log_rounds'))

        prefix = options.get('prefix', b'2b')

        return bcrypt.gensalt(rounds=rounds, prefix=prefix)

    def is_match(self, text, full_hashed_value):
        """
        gets a value indicating that given text's
        hash is identical to given full hashed value.

        :param str text: text to be hashed.

        :param bytes full_hashed_value: full hashed value to compare with.
                                        it should be in the form of
                                       `$prefix$rounds$salt-text_hash`.

        :rtype: bool
        """

        return bcrypt.checkpw(text.encode(APPLICATION_ENCODING), full_hashed_value)

    def _get_algorithm(self):
        """
        gets the hashing algorithm.

        :rtype: str
        """

        return 'bcrypt'

    def _digest_inputs(self, text, **options):
        """
        validates given inputs for bcrypt hashing and
        returns the byte equivalent of text input.
        it raises an error on invalid inputs.

        :param str text: text to be hashed.

        :raises BcryptMaxSizeLimitError: bcrypt max size limit error.

        :rtype bytes
        """

        text_bytes = text.encode(APPLICATION_ENCODING)
        size = len(text_bytes)
        if size > self.MAX_SIZE:
            raise BcryptMaxSizeLimitError('Size of input string [{text}] is [{input_size}] bytes '
                                          'which is larger than bcrypt\'s [{limit}] bytes limit.'
                                          .format(text=text, input_size=size,
                                                  limit=self.MAX_SIZE))

        return text_bytes
