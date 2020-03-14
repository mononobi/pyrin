# -*- coding: utf-8 -*-
"""
hashing handlers base module.
"""

import re

from abc import abstractmethod

from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.security.hashing.interface import AbstractHashingBase
from pyrin.settings.static import APPLICATION_ENCODING
from pyrin.utils import encoding
from pyrin.security.hashing.handlers.exceptions import InvalidHashedValueError, \
    HashingHandlerMismatchError, HashingHandlerException


class HashingBase(AbstractHashingBase):
    """
    hashing base class.
    all application hashing handlers must be subclassed from this.
    """

    # regular expression to validate format of full hashed values.
    # the following format will be matched: `$handler_name$other_parts$hashed_value`
    # note that different handlers may override this format in
    # their respective implementation.
    FORMAT_REGEX = re.compile(r'^\$[^$]+\$(.+)\$(.+)$')

    def __init__(self, **options):
        """
        initializes an instance of HashingBase.
        """

        super().__init__()

        # we set the algorithm of hashing handler as the name of it.
        self._set_name(self._get_algorithm(**options))
        self._encoding = APPLICATION_ENCODING

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

        :rtype: str
        """

        full_hashed_value = self._generate_hash(text, **options)
        return self._prepare_output(full_hashed_value, **options)

    @abstractmethod
    def _generate_hash(self, text, **options):
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

    def is_match(self, text, full_hashed_value, **options):
        """
        gets a value indicating that given text's
        hash is identical to given full hashed value.

        :param str text: text to be hashed.
        :param str full_hashed_value: full hashed value to compare with.

        :rtype: bool
        """

        try:
            self._validate_format(full_hashed_value, **options)
            hashed_part = self._get_hashed_part(self._prepare_input(full_hashed_value),
                                                **options)

            return self._is_match(text, hashed_part, **options)

        except HashingHandlerException:
            return False

    @abstractmethod
    def _is_match(self, text, hashed_value, **options):
        """
        gets a value indicating that given text's
        hash is identical to given hashed value.

        :param str text: text to be hashed.
        :param bytes hashed_value: hashed value to compare with.

        :rtype: bool
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def _get_algorithm(self, **options):
        """
        gets the hashing algorithm.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        raise CoreNotImplementedError()

    def _get_separator(self):
        """
        gets the separator used between each part of this handler's hashed result.

        :rtype: bytes
        """

        return b'$'

    def _get_separator_count(self):
        """
        gets the separator count used between parts of this handler's hashed result.

        :rtype: int
        """

        return 3

    @abstractmethod
    def _extract_parts_from_final_hash(self, full_hashed_value, **options):
        """
        extracts different parts of given full hashed value.

        :param bytes full_hashed_value: full hashed value to extract it's parts.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: tuple
        """

        raise CoreNotImplementedError()

    def _validate_format(self, full_hashed_value, **options):
        """
        validates the format of full hashed value.
        an exception will be raised on invalid values.

        :param str full_hashed_value: full hashed value to be validated.

        :raises InvalidHashedValueError: invalid hashed value error.
        """

        if not self.FORMAT_REGEX.match(full_hashed_value):
            raise InvalidHashedValueError('Input value is not a valid '
                                          '[{current}] hashing value.'
                                          .format(current=self._get_algorithm()))

    @abstractmethod
    def _get_hashed_part(self, full_hashed_value, **options):
        """
        gets the hashed part from full hashed value which current handler understands it.

        :param bytes full_hashed_value: full hashed value to get hashed part from it.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: bytes
        """

        raise CoreNotImplementedError()

    def _validate_handler(self, handler_name, **options):
        """
        validates the handler name to match the current handler.
        it will raise an error on handler mismatch.

        :param str handler_name: handler name to be validated.

        :raises HashingHandlerMismatchError: hashing handler mismatch error.
        """

        if handler_name != self._get_algorithm():
            raise HashingHandlerMismatchError('Hashing handler [{handler}] does not '
                                              'match the current handler which is [{current}].'
                                              .format(handler=handler_name,
                                                      current=self._get_algorithm()))

    def _prepare_output(self, full_hashed_value, **options):
        """
        prepares output value before returning from this handler.

        :param bytes full_hashed_value: full hashed value to be prepared.

        :rtype: str
        """

        return full_hashed_value.decode(self._encoding)

    def _prepare_input(self, full_hashed_value, **options):
        """
        prepares input value to be handled by this handler.

        :param str full_hashed_value: full hashed value to be prepared.

        :rtype: bytes
        """

        return full_hashed_value.encode(self._encoding)

    def _decode_hash_part(self, value):
        """
        decodes base64 encoded hash part into raw bytes.

        :param bytes value: base64 encoded value.

        :returns: raw bytes.
        :rtype: bytes
        """

        return encoding.base64_to_bytes(value)

    def _encode_hash_part(self, value):
        """
        encodes raw bytes hash part into base64 encoded bytes.

        :param bytes value: raw bytes value.

        :returns: base64 encoded bytes.
        :rtype: bytes
        """

        return encoding.bytes_to_base64(value)
