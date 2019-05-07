# -*- coding: utf-8 -*-
"""
pyrin exceptions module.
"""


class CoreException(Exception):
    """
    base class for all application exceptions.
    """

    def __init__(self, *args, **kwargs):
        Exception.__init__(self, *args, **kwargs)

        self._data = {}
        self._traceback = None
        self.code = self.__class__.__name__
        self.message = str(self)

    def get_code(self):
        """
        gets the error code.

        :rtype: str
        """

        return self.code

    def get_data(self):
        """
        gets the error data.

        :rtype: dict
        """

        return self._data

    def get_traceback(self):
        """
        returns the traceback of this exception.

        :rtype: object
        """

        return self._traceback

    def get_message(self):
        """
        gets the error message.

        :rtype: str
        """

        return self.message


class CoreAttributeError(CoreException, AttributeError):
    """
    core attribute error.
    """
    pass


class CoreNotImplementedError(CoreException, NotImplementedError):
    """
    core not implemented error.
    """
    pass


class CoreTypeError(CoreException, TypeError):
    """
    core type error.
    """
    pass


class CoreValueError(CoreException, ValueError):
    """
    core value error.
    """
    pass


class CoreKeyError(CoreException, KeyError):
    """
    core key error.
    """
    pass
