# -*- coding: utf-8 -*-
"""
mimetype handlers base module.
"""

from abc import abstractmethod

from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.processor.mimetype.enumerations import MIMETypeEnum
from pyrin.processor.mimetype.exceptions import InvalidMIMETypeHandlerTypeError
from pyrin.processor.mimetype.interface import AbstractMIMETypeHandlerBase


class MIMETypeHandlerBase(AbstractMIMETypeHandlerBase):
    """
    mimetype handler base class.
    """

    def __init__(self, **options):
        """
        initializes an instance of MIMETypeHandlerBase.
        """

        super().__init__()
        self._next_handler = None

    def mimetype(self, value, **options):
        """
        gets the mimetype of given value.

        returns None if it fails to detect the mimetype.

        :param object value: value to detect its mimetype.

        :rtype: str
        """

        mimetype = None
        if self.is_valid(value, **options) is True:
            mimetype = self._mimetype(value, **options)

        if mimetype is None:
            if self._next_handler is not None:
                return self._next_handler.mimetype(value, **options)
            elif isinstance(value, str):
                return MIMETypeEnum.TEXT

        return mimetype

    @abstractmethod
    def _mimetype(self, value, **options):
        """
        gets the mimetype of given value.

        returns None if it fails to detect the mimetype.

        :param object value: value to detect its mimetype.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        raise CoreNotImplementedError()

    def set_next(self, mimetype_handler):
        """
        sets the next mimetype handler and returns it.

        :param AbstractMIMETypeHandlerBase mimetype_handler: mimetype handler instance
                                                             to be set as next handler.

        :rtype: AbstractMIMETypeHandlerBase
        """

        if mimetype_handler is not None and not isinstance(mimetype_handler,
                                                           MIMETypeHandlerBase):
            raise InvalidMIMETypeHandlerTypeError('Input parameter [{instance}] is '
                                                  'not an instance of [{base}].'
                                                  .format(instance=mimetype_handler,
                                                          base=MIMETypeHandlerBase))

        self._next_handler = mimetype_handler
        return mimetype_handler

    def is_valid(self, value, **options):
        """
        gets a value indicating that the given value's type is valid for this handler.

        :param object value: value to be determined for validity.

        :rtype: bool
        """

        return isinstance(value, self.accepted_type)
