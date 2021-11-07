# -*- coding: utf-8 -*-
"""
router handlers exceptions module.
"""

from pyrin.security.exceptions import AuthenticationFailedError
from pyrin.processor.request.wrappers.exceptions import BadRequestError
from pyrin.core.exceptions import CoreException, CoreBusinessException, CoreNotFoundError


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


class FreshAuthenticationRequiredError(AuthenticationFailedError,
                                       RouterHandlerBusinessException):
    """
    fresh authentication required error.
    """
    pass


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


class ViewFunctionRequiredParamsError(BadRequestError,
                                      RouterHandlerBusinessException):
    """
    view function required params error.
    """
    pass


class InvalidRequestLimitError(RouterHandlerException):
    """
    invalid request limit error.
    """
    pass


class InvalidLifetimeError(RouterHandlerException):
    """
    invalid lifetime error.
    """
    pass


class RequestLimitOrLifetimeRequiredError(RouterHandlerException):
    """
    request limit or lifetime required error.
    """
    pass


class URLNotFoundError(CoreNotFoundError, RouterHandlerBusinessException):
    """
    url not found error.
    """
    pass


class CouldNotFindRelevantAuthenticatorError(RouterHandlerException):
    """
    could not find relevant authenticator error.
    """
    pass
