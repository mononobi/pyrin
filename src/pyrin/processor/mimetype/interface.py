# -*- coding: utf-8 -*-
"""
mimetype interface module.
"""

from abc import abstractmethod
from threading import Lock

from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.core.structs import MultiSingletonMeta, CoreObject


class MIMETypeHandlerSingletonMeta(MultiSingletonMeta):
    """
    mimetype handler singleton meta class.

    this is a thread-safe implementation of singleton.
    """

    _instances = dict()
    _lock = Lock()


class AbstractMIMETypeHandlerBase(CoreObject, metaclass=MIMETypeHandlerSingletonMeta):
    """
    abstract mimetype handler base class.
    """

    @abstractmethod
    def mimetype(self, value, **options):
        """
        gets the mimetype of given value.

        returns None if it fails to detect the mimetype.

        :param object value: value to detect its mimetype.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def set_next(self, mimetype_handler):
        """
        sets the next mimetype handler and returns it.

        :param AbstractMIMETypeHandlerBase mimetype_handler: mimetype handler instance
                                                             to be set as next handler.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: AbstractMIMETypeHandlerBase
        """

        raise CoreNotImplementedError()

    @property
    @abstractmethod
    def accepted_type(self):
        """
        gets the accepted type for this mimetype handler.

        which could detect mimetype from this type.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: type
        """

        raise CoreNotImplementedError()
