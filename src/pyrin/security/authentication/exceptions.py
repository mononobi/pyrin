# -*- coding: utf-8 -*-
"""
authentication exceptions module.
"""

from pyrin.core.enumerations import ClientErrorResponseCodeEnum
from pyrin.core.exceptions import CoreException, CoreBusinessException


class AuthenticationManagerException(CoreException):
    """
    authentication manager exception.
    """
    pass


class AuthenticationManagerBusinessException(CoreBusinessException,
                                             AuthenticationManagerException):
    """
    authentication manager business exception.
    """
    pass


class AuthenticationFailedError(AuthenticationManagerBusinessException):
    """
    authentication failed error.
    """

    def __init__(self, *args, **kwargs):
        super(CoreBusinessException, self).__init__(*args, **kwargs)
        self.code = ClientErrorResponseCodeEnum.UNAUTHORIZED


class InvalidComponentCustomKeyError(AuthenticationManagerException):
    """
    invalid component custom key.
    """
    pass
