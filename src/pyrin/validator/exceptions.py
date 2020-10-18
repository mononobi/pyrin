# -*- coding: utf-8 -*-
"""
validator exceptions module.
"""

from pyrin.core.exceptions import CoreException, CoreBusinessException


class ValidatorManagerException(CoreException):
    """
    validator manager exception.
    """
    pass


class ValidatorManagerBusinessException(CoreBusinessException,
                                        ValidatorManagerException):
    """
    validator manager business exception.
    """
    pass


class ValidationError(ValidatorManagerBusinessException):
    """
    validation error.
    """
    pass


class InvalidValidatorTypeError(ValidatorManagerException):
    """
    invalid validator type error.
    """
    pass


class DuplicatedValidatorError(ValidatorManagerException):
    """
    duplicated validator error.
    """
    pass


class ValidatorNotFoundError(ValidatorManagerException):
    """
    validator not found error.
    """
    pass


class InvalidDataForValidationError(ValidationError):
    """
    invalid data for validation error.
    """
    pass


class InvalidEntityForValidationError(ValidationError):
    """
    invalid entity for validation error.
    """
    pass


class ValidatorDomainNotFoundError(ValidatorManagerException):
    """
    validator domain not found error.
    """
    pass
