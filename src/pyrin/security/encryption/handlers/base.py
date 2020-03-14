# -*- coding: utf-8 -*-
"""
encryption handlers base module.
"""

import re

from abc import abstractmethod

import pyrin.security.utils.services as security_utils_services
import pyrin.utils.encoding as encoding_utils

from pyrin.settings.static import APPLICATION_ENCODING
from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.security.encryption.exceptions import DecryptionError
from pyrin.security.encryption.interface import AbstractEncrypterBase
from pyrin.security.encryption.handlers.exceptions import InvalidEncryptedValueError, \
    EncryptionHandlerMismatchError


class EncrypterBase(AbstractEncrypterBase):
    """
    encrypter base class.
    all application encrypters must subclass this.
    """

    # regular expression to validate format of full encrypted values.
    # the following format will be matched: `$handler_name$encrypted_value`
    FORMAT_REGEX = re.compile(r'^\$[^$]+\$(.+)$')

    def __init__(self, name, **options):
        """
        initializes an instance of EncrypterBase.

        :param str name: name of the encryption handler.
        """

        super().__init__()

        self._set_name(name)
        self._encoding = APPLICATION_ENCODING

    def _get_separator(self):
        """
        gets the separator used between each part of this handler's encryption result.

        :rtype: bytes
        """

        return b'$'

    def _get_separator_count(self):
        """
        gets the separator count used between parts of this handler's encryption result.

        :rtype: int
        """

        return 2

    @abstractmethod
    def _get_encryption_key(self, **options):
        """
        gets the signing key for encryption.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def _get_decryption_key(self, **options):
        """
        gets the signing key for decryption.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def _get_algorithm(self, **options):
        """
        gets the algorithm used for encryption.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        raise CoreNotImplementedError()

    def encrypt(self, text, **options):
        """
        encrypts the given value and returns the full encrypted
        result which includes the handler name.

        :param str text: text to be encrypted.

        :rtype: str
        """

        encrypted = self._encrypt(text, **options)
        final_result = self._make_final_result(encrypted, **options)
        return self._prepare_output(final_result)

    @abstractmethod
    def _encrypt(self, text, **options):
        """
        encrypts the given value and returns the encrypted result.

        :param str text: text to be encrypted.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: bytes
        """

        raise CoreNotImplementedError()

    def decrypt(self, full_encrypted_value, **options):
        """
        decrypts the given full encrypted value and returns the decrypted result.

        :param str full_encrypted_value: full encrypted value to be decrypted.

        :raises DecryptionError: decryption error.

        :rtype: str
        """

        try:
            self._validate_format(full_encrypted_value, **options)
            encrypted_part = self._get_encrypted_part(self._prepare_input(full_encrypted_value),
                                                      **options)

            return self._decrypt(encrypted_part, **options)
        except Exception as error:
            raise DecryptionError(error) from error

    @abstractmethod
    def _decrypt(self, value, **options):
        """
        decrypts the given value and returns the decrypted result.

        :param bytes value: value to be decrypted.

        :rtype: str
        """

        raise CoreNotImplementedError()

    def _get_encrypted_part(self, full_encrypted_value, **options):
        """
        gets the encrypted part from full encrypted value.

        :param bytes full_encrypted_value: full encrypted value to get encrypted part from it.

        :raises InvalidEncryptedValueError: invalid encrypted value error.
        :raises EncryptionHandlerMismatchError: encryption handler mismatch error.

        :rtype: bytes
        """

        handler, encrypted_part = self._extract_parts_from_final_value(
            full_encrypted_value, **options)

        self._validate_handler(handler, **options)

        return encrypted_part

    def _validate_format(self, full_encrypted_value, **options):
        """
        validates the format of full encrypted value.
        an exception will be raised on invalid values.

        :param str full_encrypted_value: full encrypted value to be validated.

        :raises InvalidEncryptedValueError: invalid encrypted value error.
        """

        if not self.FORMAT_REGEX.match(full_encrypted_value):
            raise InvalidEncryptedValueError('Input value is not a valid '
                                             '[{current}] encryption value.'
                                             .format(current=self._get_algorithm()))

    def _extract_parts_from_final_value(self, full_encrypted_value, **options):
        """
        extracts different parts from full encrypted value.

        :param bytes full_encrypted_value: full encrypted value to get different parts from it.

        :returns: tuple[str handler_name, bytes encrypted_part]
        :rtype: tuple[str, bytes]
        """

        empty, handler, encrypted_part = full_encrypted_value.split(
            self._get_separator(), self._get_separator_count())

        return handler.decode(self._encoding), self._decode_encrypted_part(encrypted_part)

    def _validate_handler(self, handler_name, **options):
        """
        validates the handler name to match the current handler.
        it will raise an error on handler mismatch.

        :param str handler_name: handler name to be validated.

        :raises EncryptionHandlerMismatchError: encryption handler mismatch error.
        """

        if handler_name != self._get_algorithm():
            raise EncryptionHandlerMismatchError('Encryption handler [{handler}] does not '
                                                 'match the current handler which is [{current}].'
                                                 .format(handler=handler_name,
                                                         current=self._get_algorithm()))

    def _make_final_result(self, encrypted_value, **options):
        """
        gets the final result by prepending the handler name to the encrypted value.

        :param bytes encrypted_value: encrypted value which handler name should be prepended to.

        :rtype: bytes
        """

        return self._get_separator() + self._get_separator().join(
            (self._get_algorithm().encode(self._encoding),
             self._encode_encrypted_part(encrypted_value)))

    def _prepare_output(self, full_encrypted_value, **options):
        """
        prepares output value before returning from this handler.

        :param bytes full_encrypted_value: full encrypted value to be prepared.

        :rtype: str
        """

        return full_encrypted_value.decode(self._encoding)

    def _prepare_input(self, full_encrypted_value, **options):
        """
        prepares input value to be handled by this handler.

        :param str full_encrypted_value: full encrypted value to be prepared.

        :rtype: bytes
        """

        return full_encrypted_value.encode(self._encoding)

    def _decode_encrypted_part(self, value):
        """
        decodes base64 encoded encrypted part into raw bytes.

        :param bytes value: base64 encoded value.

        :returns: raw bytes.
        :rtype: bytes
        """

        return encoding_utils.base64_to_bytes(value)

    def _encode_encrypted_part(self, value):
        """
        encodes raw bytes encrypted part into base64 encoded bytes.

        :param bytes value: raw bytes value.

        :returns: base64 encoded bytes.
        :rtype: bytes
        """

        return encoding_utils.bytes_to_base64(value)


class SymmetricEncrypterBase(EncrypterBase):
    """
    symmetric encrypter base class.
    this encrypter type uses a single symmetric key for encryption and decryption.
    """

    def __init__(self, **options):
        """
        initializes an instance of SymmetricEncrypterBase.
        """

        # we pass the algorithm of encryption handler as the name of it.
        super().__init__(self._get_algorithm(**options), **options)

    def _get_decryption_key(self, **options):
        """
        gets the signing key for decryption.

        :rtype: str
        """

        return self._get_encryption_key(**options)


class AsymmetricEncrypterBase(EncrypterBase):
    """
    asymmetric encrypter base class.
    this encrypter type uses a pair of public/private asymmetric
    keys for encryption and decryption.
    """

    def __init__(self, **options):
        """
        initializes an instance of AsymmetricEncrypterBase.
        """

        # we pass the algorithm of encryption handler as the name of it.
        super().__init__(self._get_algorithm(**options), **options)


class RSAEncrypterBase(AsymmetricEncrypterBase):
    """
    rsa encrypter base class.
    this encrypter type uses a pair of public/private asymmetric
    keys for encryption and decryption.
    """

    def __init__(self, **options):
        """
        initializes an instance of RSAEncrypterBase.
        """

        super().__init__(**options)

        self._private_key = None
        self._public_key = None

        self._load_keys(**options)

    def _get_encryption_key(self, **options):
        """
        gets the signing key for encryption.

        :rtype: object
        """

        return self._public_key

    def _get_decryption_key(self, **options):
        """
        gets the signing key for decryption.

        :rtype: object
        """

        return self._private_key

    def generate_key(self, **options):
        """
        generates a valid public/private key for this handler and returns it.

        :keyword int length: the length of generated key in bits.
                             if not provided, it uses default value
                             from relevant config.

        :returns: tuple[str public_key, str private_key]
        :rtype: tuple[str, str]
        """

        return security_utils_services.generate_rsa_key(**options)

    @abstractmethod
    def _load_keys(self, **options):
        """
        loads public/private keys into this class's relevant attributes.

        :raises CoreNotImplementedError: core not implemented error.
        """

        raise CoreNotImplementedError()
