# -*- coding: utf-8 -*-
"""
authorization exceptions module.
"""

from pyrin.core.enumerations import ClientErrorResponseCodeEnum
from pyrin.core.exceptions import CoreBusinessException, CoreException


class AuthorizationManagerException(CoreException):
    """
    authorization manager exception.
    """
    pass


class AuthorizationManagerBusinessException(CoreBusinessException,
                                            AuthorizationManagerException):
    """
    authorization manager business exception.
    """
    pass


class AuthorizationFailedError(AuthorizationManagerBusinessException):
    """
    authorization failed error.
    """

    def __init__(self, *args, **kwargs):
        super(AuthorizationFailedError, self).__init__(*args, **kwargs)
        self.code = ClientErrorResponseCodeEnum.FORBIDDEN
