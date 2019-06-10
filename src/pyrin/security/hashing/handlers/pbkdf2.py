# -*- coding: utf-8 -*-
"""
pbkdf2 hashing handler module.
"""

import hashlib

import pyrin.configuration.services as config_services

from pyrin.security.hashing.decorators import hashing
from pyrin.security.hashing.handlers.base import HashingBase
from pyrin.security.hashing.handlers.exceptions import InvalidHashingRoundsCountError, \
    InvalidPBKDF2InternalAlgorithmError, InvalidHashingSaltLengthError, InvalidPBKDF2HashError
from pyrin.settings.static import APPLICATION_ENCODING
from pyrin.utils import secure_random


@hashing()
class PBKDF2Hashing(HashingBase):
    """
    pbkdf2 hashing class.
    """

    def __init__(self, **options):
        """
        initializes an instance of PBKDF2Hashing.
        """

        # we pass the algorithm of hashing handler as the name of it.
        HashingBase.__init__(self, self._get_algorithm(), **options)

        # the final hash parts are separated with this byte character.
        # in the form of `$internal_algorithm$rounds$salt$text_hash`.
        self._separator = b'$'

    def generate_hash(self, text, **options):
        """
        gets the hash of input text using a random or specified salt.
        the result is in the form of `$internal_algorithm$rounds$salt$text_hash`.

        :param str text: text to be hashed.

        :keyword bytes salt: salt to be used for hashing.
                             if not provided, a random salt will be generated
                             considering `salt_length` option.

        :keyword str internal_algorithm: internal algorithm to be used
                                         for hashing. if not provided,
                                         default value from relevant
                                         config will be used.

        :keyword int rounds: rounds to perform for generating hash.
                             if not provided, default value from
                             relevant config will be used.

        :keyword int salt_length: salt length to be used for hashing.
                                  if `salt` option is provided, then
                                  this value will be ignored.
                                  if not provided, default value from
                                  relevant config will be used.

        :rtype: bytes
        """

        internal_algorithm, rounds, salt_length = self._extract_attributes(**options)
        self._validate_attributes(internal_algorithm, rounds, salt_length)

        salt = options.get('salt', None)
        if salt is None:
            salt = self._generate_salt(length=salt_length)

        text_hash = hashlib.pbkdf2_hmac(internal_algorithm,
                                        text.encode(APPLICATION_ENCODING),
                                        salt,
                                        rounds)

        return self._make_final_hash(internal_algorithm, rounds, salt, text_hash)

    def _generate_salt(self, **options):
        """
        generates a valid salt for this handler and returns it.

        :keyword int length: length of generated salt in bytes.
                             if not provided, default value from
                             relevant config will be used.

        :rtype: bytes
        """

        return secure_random.get_bytes(**options)

    def is_match(self, text, full_hashed_value):
        """
        gets a value indicating that given text's
        hash is identical to given full hashed value.

        :param str text: text to be hashed.

        :param bytes full_hashed_value: full hashed value to compare with.
                                        it should be in the form of
                                       `$internal_algorithm$rounds$salt$text_hash`.

        :rtype: bool
        """

        internal_algorithm, rounds, salt, text_hash = \
            self._extract_parts_from_final_hash(full_hashed_value)

        new_full_hashed_value = self.generate_hash(text,
                                                   internal_algorithm=internal_algorithm,
                                                   rounds=rounds, salt=salt)

        return full_hashed_value == new_full_hashed_value

    def _get_algorithm(self):
        """
        gets the hashing algorithm.

        :rtype: str
        """

        return 'PBKDF2'

    def _extract_attributes(self, **options):
        """
        extracts the required attributes for this handler from input
        keyword arguments. if not available, gets the default
        values from relevant configs.

        :keyword str internal_algorithm: internal algorithm to be used
                                         for hashing. if not provided,
                                         default value from relevant
                                         config will be used.

        :keyword int rounds: rounds to perform for generating hash.
                             if not provided, default value from
                             relevant config will be used.

        :keyword int salt_length: salt length to be used for hashing.
                                  if not provided, default value from
                                  relevant config will be used.

        :returns: tuple(str internal_algorithm, int rounds, int salt_length)

        :rtype: tuple(str, int, int)
        """

        internal_algorithm = options.get('internal_algorithm',
                                         config_services.get('security', 'hashing',
                                                             'pbkdf2_internal_algorithm'))

        rounds = options.get('rounds', config_services.get('security', 'hashing',
                                                           'pbkdf2_log_rounds'))

        salt_length = options.get('salt_length', config_services.get('security', 'hashing',
                                                                     'pbkdf2_salt_length'))

        return internal_algorithm, rounds, salt_length

    def _validate_attributes(self, internal_algorithm, rounds, salt_length):
        """
        validates the given inputs for hash generation.
        it will raise an error on invalid inputs.

        :param str internal_algorithm: internal algorithm to be used for hashing.
        :param int rounds: rounds to perform for generating hash.
        :param int salt_length: salt length to be used for hashing.

        :raises InvalidPBKDF2InternalAlgorithmError: invalid pbkdf2 internal algorithm error.
        :raises InvalidHashingRoundsCountError: invalid hashing rounds count error.
        :raises InvalidHashingSaltLengthError: invalid hashing salt length error.
        """

        if internal_algorithm not in hashlib.algorithms_guaranteed:
            raise InvalidPBKDF2InternalAlgorithmError('Internal algorithm [{algorithm}] '
                                                      'is invalid.'
                                                      .format(algorithm=internal_algorithm))

        if rounds < 1:
            raise InvalidHashingRoundsCountError('Hashing rounds [{rounds}] is invalid.'
                                                 .format(rounds=rounds))

        if salt_length < 1:
            raise InvalidHashingSaltLengthError('Salt length [{length}] is invalid.'
                                                .format(length=salt_length))

    def _make_final_hash(self, internal_algorithm, rounds, salt, text_hash):
        """
        makes final hash from input values and returns it.
        the result is in the form of `$internal_algorithm$rounds$salt$text_hash`.

        :param str internal_algorithm: internal algorithm to be used for hashing.
        :param int rounds: rounds to perform for generating hash.
        :param bytes salt: salt to be used for hashing.
        :param bytes text_hash: hash value of text and salt.

        :rtype: bytes
        """

        return self._separator + self._separator.join(
            (internal_algorithm.encode(APPLICATION_ENCODING),
             str(rounds).encode(APPLICATION_ENCODING),
             salt, text_hash))

    def _extract_parts_from_final_hash(self, full_hashed_value):
        """
        extracts different parts of given full hashed value.

        :param bytes full_hashed_value: full hashed value to extract it's parts.
                                        it must be in the form of
                                       `$internal_algorithm$rounds$salt$text_hash`.

        :returns tuple(str internal_algorithm, int rounds, bytes salt, bytes text_hash)

        :rtype: tuple(str, int, bytes, bytes)
        """

        if full_hashed_value.count(self._separator) != 4 and \
           full_hashed_value[0] != self._separator:
            raise InvalidPBKDF2HashError('Input hash value is invalid.')

        items = full_hashed_value.split(self._separator)
        internal_algorithm, rounds, salt, text_hash = tuple(items[1:])

        return internal_algorithm.decode(APPLICATION_ENCODING), int(rounds), salt, text_hash
