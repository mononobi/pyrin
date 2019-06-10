# -*- coding: utf-8 -*-
"""
encryption handlers base module.
"""

from pyrin.core.context import CoreObject
from pyrin.core.exceptions import CoreNotImplementedError


class EncrypterBase(CoreObject):
    """
    encrypter base class.
    all application encrypters must subclass this.
    """

    def __init__(self, name, **options):
        """
        initializes an instance of EncrypterBase.

        :param str name: name of the encryption handler.
        """

        CoreObject.__init__(self)

        self._set_name(name)

    def _get_encryption_key(self, **options):
        """
        gets the signing key for encryption.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        raise CoreNotImplementedError()

    def _get_decryption_key(self, **options):
        """
        gets the signing key for decryption.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        raise CoreNotImplementedError()

    def _get_algorithm(self):
        """       self._set_name(name)
        gets the algorithm used for encryption.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        raise CoreNotImplementedError()

    def encrypt(self, value):
        """
        encrypts the given value and returns the encrypted result.

        :param str value: value to be encrypted.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: bytes
        """

        raise CoreNotImplementedError()

    def decrypt(self, value):
        """
        decrypts the given value and returns the decrypted result.

        :param bytes value: value to be decrypted.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        raise CoreNotImplementedError()

    def generate_key(self, **options):
        """
        generates a valid key for this handler and returns it.

        :keyword int length: the length of generated key in bytes.
                             note that some encryption handlers may not accept custom
                             key length so this value would be ignored on those handlers.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: Union[str, tuple(str, str)]
        """

        raise CoreNotImplementedError()


class SymmetricEncrypterBase(EncrypterBase):
    """
    symmetric encrypter base class.
    this encrypter type uses a single symmetric key for encryption and decryption.
    """

    def __init__(self, name, **options):
        """
        initializes an instance of SymmetricEncrypterBase.

        :param str name: name of the encryption handler.
        """

        EncrypterBase.__init__(self, name, **options)

    def _get_decryption_key(self, **options):
        """
        gets the signing key for decryption.

        :rtype: str
        """

        return self._get_encryption_key()

    def generate_key(self, **options):
        """
        generates a valid key for this handler and returns it.

        :keyword int length: the length of generated key in bytes.
                             note that some encryption handlers may not accept custom
                             key length so this value would be ignored on those handlers.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        raise CoreNotImplementedError()


class AsymmetricEncrypterBase(EncrypterBase):
    """
    asymmetric encrypter base class.
    this encrypter type uses a pair of public/private asymmetric
    keys for encryption and decryption.
    """

    def __init__(self, name, **options):
        """
        initializes an instance of AsymmetricEncrypterBase.

        :param str name: name of the encryption handler.
        """

        EncrypterBase.__init__(self, name, **options)

    def generate_key(self, **options):
        """
        generates a valid public/private key for this handler and returns it.

        :keyword int length: the length of generated key in bytes.
                             note that some encryption handlers may not accept custom
                             key length so this value would be ignored on those handlers.

        :raises CoreNotImplementedError: core not implemented error.

        :returns tuple(str public_key, str private_key)

        :rtype: tuple(str, str)
        """

        raise CoreNotImplementedError()
