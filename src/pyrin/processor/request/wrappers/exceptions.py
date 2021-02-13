# -*- coding: utf-8 -*-
"""
request wrappers exceptions module.
"""

from pyrin.core.enumerations import ClientErrorResponseCodeEnum
from pyrin.core.exceptions import CoreException, CoreBusinessException


class RequestWrappersException(CoreException):
    """
    request wrappers exception.
    """
    pass


class RequestWrappersBusinessException(CoreBusinessException,
                                       RequestWrappersException):
    """
    request wrappers business exception.
    """
    pass


class InvalidRequestContextKeyNameError(RequestWrappersException):
    """
    invalid request context key name error.
    """
    pass


class RequestContextKeyIsAlreadyPresentError(RequestWrappersException):
    """
    request context key is already present error.
    """
    pass


class BadRequestError(RequestWrappersBusinessException):
    """
    bad request error.
    """

    def __init__(self, *args, **kwargs):
        """
        initializes an instance of BadRequestError.

        :keyword dict data: extra data for exception.
        """

        super().__init__(*args, **kwargs)
        self._code = ClientErrorResponseCodeEnum.BAD_REQUEST


class JSONBodyDecodingError(BadRequestError):
    """
    json body decoding error.
    """
    pass


class BodyDecodingError(BadRequestError):
    """
    body decoding error.
    """
    pass


class RequestDeserializationError(BadRequestError):
    """
    request deserialization error.
    """
    pass


class RequestComponentCustomKeyAlreadySetError(RequestWrappersException):
    """
    request component custom key already set error.
    """
    pass


class LargeContentError(RequestWrappersBusinessException):
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
