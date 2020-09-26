# -*- coding: utf-8 -*-
"""
validator handlers base module.
"""

import inspect

from pyrin.core.globals import _
from pyrin.database.model.base import BaseEntity
from pyrin.validator.exceptions import ValidationError
from pyrin.validator.interface import AbstractValidatorBase
from pyrin.validator.handlers.exceptions import ValidatorNameIsRequiredError, \
    ValueCouldNotBeNoneError, InvalidValueTypeError, InvalidValueError, \
    InvalidValidatorDomainError, InvalidAcceptedTypeError, InvalidValidationExceptionTypeError


class ValidatorBase(AbstractValidatorBase):
    """
    validator base class.

    all application validators must be subclassed from this.
    """

    invalid_type_error = InvalidValueTypeError
    invalid_type_message = _('The provided value for [{param_name}] '
                             'is not an instance of {type}.')
    none_value_error = ValueCouldNotBeNoneError
    none_value_message = _('The provided value for [{param_name}] could not be None.')

    default_nullable = None
    default_localized_name = None

    def __init__(self, domain, name, **options):
        """
        initializes an instance of ValidatorBase.

        :param type[BaseEntity] | str domain: the domain in which this validator
                                              must be registered. it could be a
                                              type of a BaseEntity subclass.
                                              if a validator must be registered
                                              independent from any BaseEntity subclass,
                                              the domain could be a unique string name.
                                              note that the provided string name must be
                                              unique at application level.

        :param str name: validator name.
                         each validator will be registered with its name
                         in corresponding domain.
                         to enable automatic validations, the provided
                         name must be the exact name of the parameter
                         which this validator will validate.

        :keyword type | tuple[type] accepted_type: accepted type for value.
                                                   no type checking will be
                                                   done if not provided.

        :keyword bool nullable: specifies that null values should be accepted as valid.
                                defaults to True if not provided.

        :keyword str localized_name: localized name of the parameter
                                     which this validator will validate.
                                     it must be passed using `_` method
                                     from `pyrin.core.globals`.
                                     defaults to `name` if not provided.

        :raises ValidatorNameIsRequiredError: validator name is required error.
        :raises InvalidValidatorDomainError: invalid validator domain error.
        :raises InvalidAcceptedTypeError: invalid accepted type error.
        :raises InvalidValidationExceptionTypeError: invalid validation exception type error.
        """

        if name in (None, '') or name.isspace():
            raise ValidatorNameIsRequiredError('Validator name must be provided.')

        if (not inspect.isclass(domain) or not issubclass(domain, BaseEntity)) and \
                (not isinstance(domain, str) or domain.isspace()):
            raise InvalidValidatorDomainError('The provided domain for validator [{name}] is '
                                              'not an instance of [{entity}] or [{string}].'
                                              .format(name=name, entity=BaseEntity, string=str))

        nullable = options.get('nullable')
        if nullable is None:
            if self.default_nullable is not None:
                nullable = self.default_nullable
            else:
                nullable = True

        accepted_type = options.get('accepted_type')
        if accepted_type is not None and not isinstance(accepted_type, (type, tuple)):
            raise InvalidAcceptedTypeError('The provided accepted type '
                                           '[{accepted_type}] must be a type '
                                           'or tuple of types.'
                                           .format(accepted_type=accepted_type))

        if isinstance(accepted_type, tuple):
            if len(accepted_type) <= 0:
                raise InvalidAcceptedTypeError('The provided accepted type tuple '
                                               'should have at least one item in it.'
                                               'if no type checking should be done, '
                                               'do not provide the accepted type '
                                               'keyword argument.')
            for item in accepted_type:
                if not isinstance(item, type):
                    raise InvalidAcceptedTypeError('The provided accepted type '
                                                   '[{accepted_type}] must be a type'
                                                   .format(accepted_type=accepted_type))

        localized_name = options.get('localized_name') or self.default_localized_name
        if localized_name in (None, '') or localized_name.isspace():
            localized_name = _(name)

        self._validate_exception_type(self.invalid_type_error)
        self._validate_exception_type(self.none_value_error)

        super().__init__()
        self._set_name(name)
        self._domain = domain
        self._nullable = nullable
        self._accepted_type = accepted_type
        self._localized_name = localized_name

    def validate(self, value, **options):
        """
        validates the given value.

        it raises an error if validation fails.

        :param object value: value to be validated.

        :keyword bool nullable: determines that provided value could be None.
                                this value has precedence over `nullable`
                                instance attribute if provided.

        :raises InvalidValueTypeError: invalid value type error.
        :raises InvalidValueError: invalid value error.
        :raises ValueCouldNotBeNoneError: value could not be none error.
        :raises ValidationError: validation error.
        """

        nullable = options.pop('nullable', None)
        if nullable is None:
            nullable = self.nullable

        if value is not None:
            self._validate_type(value)
            try:
                self._validate(value, **options)
            except ValidationError as error:
                raise error
            except Exception:
                raise InvalidValueError(_('The provided value for '
                                          '[{param_name}] is invalid.').
                                        format(param_name=self.localized_name))
        elif nullable is True:
            return
        else:
            raise self.none_value_error(
                self.none_value_message.format(param_name=self.localized_name))

    def _validate(self, value, **options):
        """
        validates the given value.

        it raises an error if validation fails.
        the raised error must be an instance of ValidationError.
        this method must be implemented in subclasses.
        each overridden method must call `super()._validate()`
        preferably at the beginning.
        if no extra validation is needed, it could be left unimplemented.

        :param object value: value to be validated.

        :raises ValidationError: validation error.
        """
        pass

    def _validate_type(self, value):
        """
        validates the type of given value.

        if no accepted type is set for this validator, this method does nothing.

        :param object value: value to be validated.

        :raises InvalidValueTypeError: invalid value type error.
        """

        if self.accepted_type is None:
            return

        if not isinstance(value, self.accepted_type):
            preview_type = None
            if isinstance(self.accepted_type, tuple):
                preview_type = list(self.accepted_type)
            else:
                preview_type = [self.accepted_type]

            raise self.invalid_type_error(self.invalid_type_message.format(
                param_name=self.localized_name, type=preview_type))

    def _validate_exception_type(self, exception):
        """
        asserts that given exception type is subclassed from ValidationError.

        :param type[CoreException] exception: exception to validate its type.

        :raises InvalidValidationExceptionTypeError: invalid validation exception type error.
        """

        if not issubclass(exception, ValidationError):
            raise InvalidValidationExceptionTypeError('The specified validation exception '
                                                      '[{exception}] is not a subclass of '
                                                      '[{base}].'
                                                      .format(exception=exception,
                                                              base=ValidationError))

    @property
    def name(self):
        """
        gets the name of this validator.

        :rtype: str
        """

        return self.get_name()

    @property
    def domain(self):
        """
        gets the domain of this validator.

        domain is the type of a BaseEntity subclass that
        this validator validates a value of it.
        if a validator is not specific to an entity, then
        domain could be a unique string name.

        :rtype: type[BaseEntity] | str
        """

        return self._domain

    @property
    def nullable(self):
        """
        gets a value indicating that null values must be accepted as valid.

        :rtype: bool
        """

        return self._nullable

    @property
    def accepted_type(self):
        """
        gets the accepted type for this validator.

        returns None if no type checking is defined for this validator.

        :rtype: type | tuple[type]
        """

        return self._accepted_type

    @property
    def localized_name(self):
        """
        gets the localized name of this validator.

        :rtype: str
        """

        return self._localized_name
