# -*- coding: utf-8 -*-
"""
hashing handlers base module.
"""

from pyrin.core.context import CoreObject
from pyrin.core.exceptions import CoreNotImplementedError


class HashingBase(CoreObject):
    """
    hashing base class.
    all application hashing handlers must be subclassed from this.
    """

    def __init__(self, name, **options):
        """
        initializes an instance of HashingBase.

        :param str name: name of the hashing handler.
        """

        CoreObject.__init__(self)

        self._set_name(name)

    def generate_hash(self, text, **options):
        """
        gets the hash of input text using a random or specified salt.

        :param str text: text to be hashed.

        :keyword bytes salt: salt to be used for hashing.
                             if not provided, a random salt will be generated
                             considering `salt_length` option.

        :keyword int rounds: rounds to perform for generating hash.
                             if not provided, default value from
                             relevant config will be used.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: bytes
        """

        raise CoreNotImplementedError()

    def is_match(self, text, full_hashed_value):
        """
        gets a value indicating that given text's
        hash is identical to given full hashed value.

        :param str text: text to be hashed.
        :param bytes full_hashed_value: full hashed value to compare with.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: bool
        """

        raise CoreNotImplementedError()

    def _get_algorithm(self):
        """
        gets the hashing algorithm.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        raise CoreNotImplementedError()
