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
        super(LargeContentError, self).__init__(*args, **kwargs)
        self.code = ClientErrorResponseCodeEnum.PAYLOAD_TOO_LARGE


class PermissionTypeError(RouterHandlerException):
    """
    permission type error.
    """
    pass
