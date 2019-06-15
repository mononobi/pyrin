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


class PermissionDeniedError(AuthorizationManagerBusinessException):
    """
    permission denied error.
    """

    def __init__(self, *args, **kwargs):
        super(PermissionDeniedError, self).__init__(*args, **kwargs)
        self.code = ClientErrorResponseCodeEnum.FORBIDDEN
