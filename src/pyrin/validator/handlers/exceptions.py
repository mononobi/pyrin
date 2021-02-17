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


class HandlersValidationException(ValidationError,
                                  ValidatorHandlersBusinessException):
    """
    handlers validation exception.

    this class should be used as the base class for all handlers validation errors.
    """
    pass


class ValidatorNameIsRequiredError(ValidatorHandlersException):
    """
    validator name is required error.
    """
    pass


class ValueCouldNotBeNoneError(HandlersValidationException):
    """
    value could not be none error.
    """
    pass


class ValueIsNotListError(HandlersValidationException):
    """
    value is not list error.
    """
    pass


class ValueCouldNotBeAnEmptyListError(HandlersValidationException):
    """
    value could not be an empty list error.
    """
    pass


class ValueIsLowerThanMinimumError(HandlersValidationException):
    """
    value is lower than minimum error.
    """
    pass


class ValueIsHigherThanMaximumError(HandlersValidationException):
    """
    value is higher than maximum error.
    """
    pass


class ValueIsOutOfRangeError(HandlersValidationException):
    """
    value is out of range error.
    """
    pass


class InvalidValueTypeError(HandlersValidationException):
    """
    invalid value type error.
    """
    pass


class ValueDoesNotMatchPatternError(HandlersValidationException):
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


class ValidatorFixerMustBeCallable(ValidatorHandlersException):
    """
    validator fixer must be callable.
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


class LongStringLengthError(HandlersValidationException):
    """
    long string length error.
    """
    pass


class ShortStringLengthError(HandlersValidationException):
    """
    short string length error.
    """
    pass


class ValueCouldNotBeBlankError(HandlersValidationException):
    """
    value could not be blank error.
    """
    pass


class ValueCouldNotBeWhitespaceError(HandlersValidationException):
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


class ValueIsNotNumberError(InvalidValueTypeError):
    """
    value is not number error.
    """
    pass


class ValueIsNotIntegerError(InvalidValueTypeError):
    """
    value is not integer error.
    """
    pass


class ValueIsNotFloatError(InvalidValueTypeError):
    """
    value is not float error.
    """
    pass


class ValueIsNotStringError(InvalidValueTypeError):
    """
    value is not string error.
    """
    pass


class ValueIsNotDateTimeError(InvalidValueTypeError):
    """
    value is not datetime error.
    """
    pass


class ValueIsNotDateError(InvalidValueTypeError):
    """
    value is not date error.
    """
    pass


class ValueIsNotTimeError(InvalidValueTypeError):
    """
    value is not time error.
    """
    pass


class ValueIsNotBooleanError(InvalidValueTypeError):
    """
    value is not boolean error.
    """
    pass


class ValueIsNotUUIDError(InvalidValueTypeError):
    """
    value is not uuid error.
    """
    pass


class ValueIsNotUUID4Error(InvalidValueTypeError):
    """
    value is not uuid4 error.
    """
    pass


class MinimumLengthHigherThanMaximumLengthError(ValidatorHandlersException):
    """
    minimum length higher than maximum length error.
    """
    pass


class MinimumValueLargerThanMaximumValueError(ValidatorHandlersException):
    """
    minimum value larger than maximum value error.
    """
    pass


class InvalidEmailError(HandlersValidationException):
    """
    invalid email error.
    """
    pass


class InvalidIPv4Error(HandlersValidationException):
    """
    invalid ipv4 error.
    """
    pass


class InvalidURLError(HandlersValidationException):
    """
    invalid url error.
    """
    pass


class InvalidHTTPURLError(InvalidURLError):
    """
    invalid http url error.
    """
    pass


class InvalidHTTPSURLError(InvalidURLError):
    """
    invalid https url error.
    """
    pass
