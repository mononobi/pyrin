# -*- coding: utf-8 -*-
"""
encryption interface module.
"""

from abc import abstractmethod
from threading import Lock

from pyrin.core.structs import CoreObject, MultiSingletonMeta
from pyrin.core.exceptions import CoreNotImplementedError


class EncrypterSingletonMeta(MultiSingletonMeta):
    """
    encrypter singleton meta class.
    this is a thread-safe implementation of singleton.
    """

    _instances = dict()
    _lock = Lock()


class AbstractEncrypterBase(CoreObject, metaclass=EncrypterSingletonMeta):
    """
    abstract encrypter base class.
    all application encrypters must subclass this.
    """

    @abstractmethod
    def encrypt(self, text, **options):
        """
        encrypts the given value and returns the full encrypted
        result which includes the handler name.

        :param str text: text to be encrypted.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def decrypt(self, full_encrypted_value, **options):
        """
        decrypts the given full encrypted value and returns the decrypted result.

        :param str full_encrypted_value: full encrypted value to be decrypted.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def generate_key(self, **options):
        """
        generates a valid key for this handler and returns it.

        :keyword int length: the length of generated key in bytes.
                             note that some encryption handlers may
                             not accept custom key length so this
                             value would be ignored on those handlers.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str | tuple[str, str]
        """

        raise CoreNotImplementedError()
