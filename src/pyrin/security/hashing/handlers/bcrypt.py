# -*- coding: utf-8 -*-
"""
bcrypt hashing handler module.
"""

import re

import bcrypt

import pyrin.configuration.services as config_services

from pyrin.security.hashing.decorators import hashing
from pyrin.security.hashing.handlers.base import HashingBase
from pyrin.security.hashing.handlers.exceptions import BcryptMaxSizeLimitError


@hashing()
class BcryptHashing(HashingBase):
    """
    bcrypt hashing class.
    """

    # regular expression to validate format of full hashed values.
    # the following format will be matched:
    # `$handler_name$prefix$rounds$salt-text_plus_salt_hash`
    FORMAT_REGEX = re.compile(r'^\$bcrypt\$[^$]+\$[\d]+\$(.+)$')

    # bcrypt hashing has a max size limit that could be hashed, original
    # implementation truncates the input string to satisfy max size limit.
    # since the max size is different on each bcrypt implementation,
    # we consider 50 bytes as a safe max size for all implementations.
    # 50 bytes is equivalent to 50 chars in ascii encoding, not unicode.
    MAX_SIZE = 50

    def __init__(self, **options):
        """
        initializes an instance of BcryptHashing.
        """

        super().__init__(**options)

    def _generate_hash(self, text, **options):
        """
        gets the hash of input text using a random or specified salt.

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

        bcrypt_hash = bcrypt.hashpw(text_bytes, salt)
        return self._make_final_hash(bcrypt_hash)

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
                                                           'bcrypt_rounds'))

        prefix = options.get('prefix', b'2b')

        return bcrypt.gensalt(rounds=rounds, prefix=prefix)

    def _is_match(self, text, hashed_value, **options):
        """
        gets a value indicating that given text's
        hash is identical to given hashed value.

        :param str text: text to be hashed.
        :param bytes hashed_value: hashed value to compare with.

        :rtype: bool
        """

        return bcrypt.checkpw(text.encode(self._encoding), hashed_value)

    def _get_algorithm(self, **options):
        """
        gets the hashing algorithm.

        :rtype: str
        """

        return 'bcrypt'

    def _get_separator_count(self):
        """
        gets the separator count used between parts of this handler's hashed result.

        :rtype: int
        """

        return 4

    def _digest_inputs(self, text, **options):
        """
        validates given inputs for bcrypt hashing and
        returns the byte equivalent of text input.
        it raises an error on invalid inputs.

        :param str text: text to be hashed.

        :raises BcryptMaxSizeLimitError: bcrypt max size limit error.

        :rtype: bytes
        """

        text_bytes = text.encode(self._encoding)
        size = len(text_bytes)
        if size > self.MAX_SIZE:
            raise BcryptMaxSizeLimitError('Size of input string is [{input_size}] bytes '
                                          'which is larger than bcrypt\'s [{limit}] bytes limit.'
                                          .format(input_size=size,
                                                  limit=self.MAX_SIZE))

        return text_bytes

    def _get_hashed_part(self, full_hashed_value, **options):
        """
        gets the hashed part from full hashed value which current handler understands it.
        this method returns the original hash value made by bcrypt
        excluding the handler name.

        :param bytes full_hashed_value: full hashed value to get hashed part from it.

        :rtype: bytes
        """

        empty, handler, bcrypt_hash = full_hashed_value.split(self._get_separator(), 2)
        return self._get_separator() + bcrypt_hash

    def _make_final_hash(self, bcrypt_hash, **options):
        """
        makes final hash from input values and returns it.

        :param bytes bcrypt_hash: hash value which is generated by bcrypt algorithm.

        :rtype: bytes
        """

        return self._get_separator() + self._get_algorithm().encode(
            self._encoding) + bcrypt_hash
