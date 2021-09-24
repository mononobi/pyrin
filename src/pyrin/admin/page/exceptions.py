# -*- coding: utf-8 -*-
"""
admin page exceptions module.
"""

from pyrin.core.exceptions import CoreException, CoreBusinessException
from pyrin.validator.exceptions import ValidationError


class AdminPageException(CoreException):
    """
    admin page exception.
    """
    pass


class AdminPageBusinessException(CoreBusinessException,
                                 AdminPageException):
    """
    admin page business exception.
    """
    pass


class InvalidListFieldError(AdminPageException):
    """
    invalid list field error.
    """
    pass


class InvalidListSearchFieldError(AdminPageException):
    """
    invalid list search field error.
    """
    pass


class ListFieldRequiredError(AdminPageException):
    """
    list field required error.
    """
    pass


class InvalidMethodNameError(AdminPageException):
    """
    invalid method name error.
    """
    pass


class InvalidAdminEntityTypeError(AdminPageException):
    """
    invalid admin entity type error.
    """
    pass


class AdminRegisterNameRequiredError(AdminPageException):
    """
    admin register name required error.
    """
    pass


class AdminNameRequiredError(AdminPageException):
    """
    admin name required error.
    """
    pass


class RequiredValuesNotProvidedError(ValidationError, AdminPageBusinessException):
    """
    required values not provided error.
    """
    pass


class CompositePrimaryKeysNotSupportedError(AdminPageException):
    """
    composite primary keys not supported error.
    """
    pass


class DuplicateListFieldNamesError(AdminPageException):
    """
    duplicate list field names error.
    """
    pass


class DuplicateListSearchFieldNamesError(AdminPageException):
    """
    duplicate list search field names error.
    """
    pass


class InvalidListFieldNameError(AdminPageException):
    """
    invalid list field name error.
    """
    pass


class EntityNotFoundError(AdminPageBusinessException):
    """
    entity not found error.
    """
    pass


class ExtraDataFieldsAndEntityFieldsOverlapError(AdminPageException):
    """
    extra data fields and entity fields overlap error.
    """
    pass
