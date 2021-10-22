# -*- coding: utf-8 -*-
"""
admin users exceptions module.
"""

from pyrin.validator.exceptions import ValidationError
from pyrin.core.exceptions import CoreBusinessException, CoreException
from pyrin.security.authentication.exceptions import AuthenticationFailedError


class AdminUsersManagerException(CoreException):
    """
    admin users manager exception.
    """
    pass


class AdminUsersManagerBusinessException(CoreBusinessException,
                                         AdminUsersManagerException):
    """
    admin users manager business exception.
    """
    pass


class AdminUserNotFoundError(AuthenticationFailedError,
                             AdminUsersManagerBusinessException):
    """
    admin user not found error.
    """
    pass


class PasswordsDoNotMatchError(ValidationError,
                               AdminUsersManagerBusinessException):
    """
    passwords do not match error.
    """
    pass
