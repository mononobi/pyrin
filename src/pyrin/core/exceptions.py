# -*- coding: utf-8 -*-
"""
core exceptions module.
"""

from pyrin.core.enumerations import ServerErrorResponseCodeEnum, ClientErrorResponseCodeEnum


class CoreException(Exception):
    """
    base class for all application exceptions.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._data = {}
        self._traceback = None
        self.code = ServerErrorResponseCodeEnum.INTERNAL_SERVER_ERROR
        self.description = str(self)

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

    def get_description(self):
        """
        gets the error description.

        :rtype: str
        """

        return self.description


class CoreBusinessException(CoreException):
    """
    base class for all application business exceptions.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code = ClientErrorResponseCodeEnum.UNPROCESSABLE_ENTITY


class CoreAttributeError(CoreException, AttributeError):
    """
    core attribute error.
    """
    pass


class ContextAttributeError(CoreAttributeError):
    """
    context attribute error.
    """
    pass


class CoreNotImplementedError(CoreException, NotImplementedError):
    """
    core not implemented error.
    """

    def __init__(self, *args, **kwargs):
        super().__init__('This method does not have an implementation.',
                         *args, **kwargs)


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


class CoreAssertionError(CoreException, AssertionError):
    """
    core assertion error.
    """
    pass


class CoreNotADirectoryError(CoreException, NotADirectoryError):
    """
    core not a directory error.
    """
    pass


class CoreFileNotFoundError(CoreException, FileNotFoundError):
    """
    core file not found error.
    """
    pass


class CoreNameError(CoreException, NameError):
    """
    core name error.
    """
    pass


class InvalidHookTypeError(CoreException):
    """
    invalid hook type error.
    """
    pass
