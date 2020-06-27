# -*- coding: utf-8 -*-
"""
validator handlers exceptions module.
"""

from pyrin.core.exceptions import CoreException, CoreBusinessException

from pyrin.validator.exceptions import ValidationError


class ValidatorHandlersException(CoreException):
    """
    validator handlers exception.
    """
    pass


class ValidatorHandlersBusinessException(CoreBusinessException,
                                         ValidatorHandlersException):
    """
    validator handlers business exception.
    """
    pass


class ValidatorNameIsRequiredError(ValidatorHandlersException):
    """
    validator name is required error.
    """
    pass


class ValueCouldNotBeNoneError(ValidatorHandlersBusinessException,
                               ValidationError):
    """
    value could not be none error.
    """
    pass


class ValueIsLowerThanMinimumError(ValidatorHandlersBusinessException,
                                   ValidationError):
    """
    value is lower than minimum error.
    """
    pass


class ValueIsHigherThanMaximumError(ValidatorHandlersBusinessException,
                                    ValidationError):
    """
    value is higher than maximum error.
    """
    pass


class ValueIsOutOfRangeError(ValidatorHandlersBusinessException,
                             ValidationError):
    """
    value is out of range error.
    """
    pass


class InvalidValueTypeError(ValidatorHandlersBusinessException,
                            ValidationError):
    """
    invalid value type error.
    """
    pass


class InvalidValueError(ValidatorHandlersBusinessException,
                        ValidationError):
    """
    invalid value error.
    """
    pass


class ValueDoesNotMatchPatternError(ValidatorHandlersBusinessException,
                                    ValidationError):
    """
    value does not match pattern error.
    """
    pass


class InvalidValidatorDomainError(ValidatorHandlersException):
    """
    invalid validator domain error.
    """
    pass


class InvalidAcceptedTypeError(ValidatorHandlersException):
    """
    invalid accepted type error.
    """
    pass


class InvalidValidationExceptionTypeError(ValidatorHandlersException):
    """
    invalid validation exception type error.
    """
    pass


class AcceptedMinimumValueMustBeProvidedError(ValidatorHandlersException):
    """
    accepted minimum value must be provided error.
    """
    pass


class AcceptedMaximumValueMustBeProvidedError(ValidatorHandlersException):
    """
    accepted maximum value must be provided error.
    """
    pass


class ValidValuesMustBeProvidedError(ValidatorHandlersException):
    """
    valid values must be provided error.
    """
    pass


class InvalidValuesMustBeProvidedError(ValidatorHandlersException):
    """
    invalid values must be provided error.
    """
    pass


class InvalidStringLengthError(ValidatorHandlersBusinessException,
                               ValidationError):
    """
    invalid string length error.
    """
    pass


class ValueCouldNotBeBlankError(ValidatorHandlersBusinessException,
                                ValidationError):
    """
    value could not be blank error.
    """
    pass


class ValueCouldNotBeWhitespaceError(ValidatorHandlersBusinessException,
                                     ValidationError):
    """
    value could not be whitespace error.
    """
    pass


class InvalidRegularExpressionError(ValidatorHandlersException):
    """
    invalid regular expression error.
    """
    pass


class RegularExpressionMustBeProvidedError(ValidatorHandlersException):
    """
    regular expression must be provided error.
    """
    pass
