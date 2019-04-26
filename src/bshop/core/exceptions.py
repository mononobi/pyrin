# -*- coding: utf-8 -*-
"""
Core exceptions module.
"""


class CoreException(Exception):
    """
    Base class for all application exceptions.
    """

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

        self._data = {}
        self._traceback = None
        self.code = self.__class__.__name__
        self.message = str(self)

    def get_code(self):
        """
        Gets the error code.

        :rtype: str
        """

        return self.code

    def get_data(self):
        """
        Gets the error data.

        :rtype: dict
        """

        return self._data

    def get_traceback(self):
        """
        Returns the traceback of this exception.

        :rtype: object
        """

        return self._traceback

    def get_message(self):
        """
        Gets the error message.

        :rtype: str
        """

        return self.message


class CoreAttributeError(CoreException, AttributeError):
    """
    Core attribute error.
    """
    pass


class CoreNotImplementedError(CoreException, NotImplementedError):
    """
    Core not implemented error.
    """
    pass


class CoreTypeError(CoreException, TypeError):
    """
    Core type error.
    """
    pass


class CoreValueError(CoreException, ValueError):
    """
    Core value error.
    """
    pass
