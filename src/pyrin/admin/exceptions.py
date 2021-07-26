# -*- coding: utf-8 -*-
"""
admin exceptions module.
"""

from pyrin.api.router.handlers.exceptions import URLNotFoundError
from pyrin.core.exceptions import CoreException, CoreBusinessException, \
    CoreMethodNotAllowedError


class AdminManagerException(CoreException):
    """
    admin manager exception.
    """
    pass


class AdminManagerBusinessException(CoreBusinessException,
                                    AdminManagerException):
    """
    admin manager business exception.
    """
    pass


class InvalidAdminPageTypeError(AdminManagerException):
    """
    invalid admin page type error.
    """
    pass


class DuplicatedAdminPageError(AdminManagerException):
    """
    duplicated admin page error.
    """
    pass


class AdminPageNotFoundError(URLNotFoundError, AdminManagerBusinessException):
    """
    admin page not found error.
    """
    pass


class AdminOperationNotAllowedError(CoreMethodNotAllowedError, AdminManagerBusinessException):
    """
    admin operation not allowed error.
    """
    pass


class AdminPagesHaveNotLoadedError(AdminManagerException):
    """
    admin pages have not loaded error.
    """
    pass
