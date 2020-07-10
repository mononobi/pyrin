# -*- coding: utf-8 -*-
"""
router handlers exceptions module.
"""

from pyrin.core.enumerations import ClientErrorResponseCodeEnum
from pyrin.core.exceptions import CoreException, CoreBusinessException
from pyrin.security.authentication.exceptions import AuthenticationFailedError


class RouterHandlerException(CoreException):
    """
    router handler exception.
    """
    pass


class RouterHandlerBusinessException(CoreBusinessException,
                                     RouterHandlerException):
    """
    router handler business exception.
    """
    pass


class InvalidViewFunctionTypeError(RouterHandlerException):
    """
    invalid view function type error.
    """
    pass


class MaxContentLengthLimitMismatchError(RouterHandlerException):
    """
    max content length limit mismatch error.
    """
    pass


class FreshTokenRequiredError(AuthenticationFailedError,
                              RouterHandlerBusinessException):
    """
    fresh token required error.
    """
    pass


class LargeContentError(RouterHandlerBusinessException):
    """
    large content error.
    """

    def __init__(self, *args, **kwargs):
        """
        initializes an instance of LargeContentError.

        :keyword dict data: extra data for exception.
        """

        super().__init__(*args, **kwargs)
        self._code = ClientErrorResponseCodeEnum.PAYLOAD_TOO_LARGE


class PermissionTypeError(RouterHandlerException):
    """
    permission type error.
    """
    pass


class InvalidResultSchemaTypeError(RouterHandlerException):
    """
    invalid result schema type error.
    """
    pass


class RouteIsNotBoundedError(RouterHandlerException):
    """
    route is not bounded error.
    """
    pass


class RouteIsNotBoundedToMapError(RouterHandlerException):
    """
    route is not bounded to map error.
    """
    pass


class InvalidResponseStatusCodeError(RouterHandlerException):
    """
    invalid response status code error.
    """
    pass
