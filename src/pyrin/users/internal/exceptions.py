# -*- coding: utf-8 -*-
"""
users internal exceptions module.
"""

from pyrin.validator.exceptions import ValidationError
from pyrin.core.exceptions import CoreBusinessException, CoreException


class InternalUsersManagerException(CoreException):
    """
    internal users manager exception.
    """
    pass


class InternalUsersManagerBusinessException(CoreBusinessException,
                                            InternalUsersManagerException):
    """
    internal users manager business exception.
    """
    pass


class InternalUserNotFoundError(InternalUsersManagerBusinessException):
    """
    internal user not found error.
    """
    pass


class PasswordsDoNotMatchError(ValidationError,
                               InternalUsersManagerBusinessException):
    """
    passwords do not match error.
    """
    pass
