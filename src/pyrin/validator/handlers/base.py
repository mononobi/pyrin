# -*- coding: utf-8 -*-
"""
validator handlers base module.
"""

import inspect

import pyrin.utils.misc as misc_utils

from pyrin.core.globals import _, LIST_TYPES
from pyrin.database.model.base import BaseEntity
from pyrin.validator.exceptions import ValidationError
from pyrin.validator.interface import AbstractValidatorBase
from pyrin.validator.handlers.exceptions import ValidatorNameIsRequiredError, \
    ValueCouldNotBeNoneError, InvalidValueTypeError, InvalidValidatorDomainError, \
    InvalidAcceptedTypeError, InvalidValidationExceptionTypeError, ValueIsNotListError


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
    not_list_error = ValueIsNotListError
    not_list_message = _('The provided value for [{param_name}] must be a list of items.')

    default_nullable = None
    default_localized_name = None
    default_is_list = False
    default_null_items = False

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

        :keyword bool is_list: specifies that the value must be a list of items.
                               defaults to False if not provided.

        :keyword bool null_items: specifies that list items could be None.
                                  it is only used if `is_list=True` is provided.
                                  defaults to False if not provided.

        :raises ValidatorNameIsRequiredError: validator name is required error.
        :raises InvalidValidatorDomainError: invalid validator domain error.
        :raises InvalidAcceptedTypeError: invalid accepted type error.
        :raises InvalidValidationExceptionTypeError: invalid validation exception type error.
        """

        if name in (None, '') or name.isspace():
            raise ValidatorNameIsRequiredError('Validator name must be provided for validator '
                                               '[{instance}].'.format(instance=self))

        if (not inspect.isclass(domain) or not issubclass(domain, BaseEntity)) and \
                (not isinstance(domain, str) or domain.isspace()):
            raise InvalidValidatorDomainError('The provided domain for validator [{instance}] '
                                              'with name [{name}] is not a subclass of '
                                              '[{entity}] or a string value.'
                                              .format(instance=self, name=name,
                                                      entity=BaseEntity))

        nullable = options.get('nullable')
        if nullable is None:
            if self.default_nullable is not None:
                nullable = self.default_nullable
            else:
                nullable = True

        is_list = options.get('is_list')
        if is_list is None:
            if self.default_is_list is not None:
                is_list = self.default_is_list
            else:
                is_list = False

        null_items = options.get('null_items')
        if null_items is None:
            if self.default_null_items is not None:
                null_items = self.default_null_items
            else:
                null_items = False

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
        self._validate_exception_type(self.not_list_error)

        super().__init__()
        self._set_name(name)
        self._domain = domain
        self._nullable = nullable
        self._accepted_type = accepted_type
        self._localized_name = localized_name
        self._is_list = is_list
        self._null_items = null_items

    def validate(self, value, **options):
        """
        validates the given value.

        it raises an error if validation fails.

        :param object value: value to be validated.

        :keyword bool nullable: determines that provided value could be None.
                                this value has precedence over `nullable`
                                instance attribute if provided.

        :keyword bool is_list: specifies that the value must be a list of items.
                               this value has precedence over `is_list`
                               instance attribute if provided.

        :keyword bool null_items: specifies that list items could be None.
                                  it is only used if `is_list=True` is provided.
                                  this value has precedence over `null_items`
                                  instance attribute if provided.

        :raises ValueIsNotListError: value is not list error.
        :raises InvalidValueTypeError: invalid value type error.
        :raises ValueCouldNotBeNoneError: value could not be none error.
        :raises ValidationError: validation error.
        """

        nullable = options.pop('nullable', None)
        if nullable is None:
            nullable = self.nullable

        is_list = options.pop('is_list', None)
        if is_list is None:
            is_list = self.is_list

        null_items = options.pop('null_items', None)
        if null_items is None:
            null_items = self.null_items

        if value is None:
            return self._validate_nullable(value, nullable)

        if is_list is True and (not isinstance(value, list) or len(value) <= 0):
            raise self.not_list_error(
                self.not_list_message.format(param_name=self.localized_name))

        if is_list is not True:
            self._perform_validation(value, nullable, **options)
        else:
            for item in value:
                self._perform_validation(item, null_items, **options)

    def _perform_validation(self, value, nullable, **options):
        """
        performs validation on given value.

        it raises an error if validation fails.

        :param object value: value to be validated.
        :param bool nullable: determines that provided value could be None.

        :raises InvalidValueTypeError: invalid value type error.
        :raises ValueCouldNotBeNoneError: value could not be none error.
        :raises ValidationError: validation error.
        """

        if value is None:
            return self._validate_nullable(value, nullable)

        self._validate_type(value)
        self._validate(value, **options)

    def _validate_nullable(self, value, nullable):
        """
        validates value for nullability.

        it raises an error if validation fails.

        :param object value: value to be validated.
        :param bool nullable: determines that provided value could be None.

        :raises ValueCouldNotBeNoneError: value could not be none error.
        """

        if nullable is False and value is None:
            raise self.none_value_error(self.none_value_message.format(
                param_name=self.localized_name))

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
            preview_type = misc_utils.make_iterable(self.accepted_type, list)

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

    def _get_representation(self, value):
        """
        gets the string representable version of input value.

        :param object value: value to get its string representation.

        :returns: string representable value.
        """

        if not isinstance(value, self.accepted_type):
            return value

        return self._get_safe_representation(value)

    def _get_safe_representation(self, value):
        """
        gets the string representable version of input value.

        this method is intended to be overridden in subclasses for complex types.
        the type of value is guaranteed to be what subclasses are expecting.

        :param object value: value to get its string representation.

        :returns: string representable value.
        """

        return value

    def _get_list_representation(self, value):
        """
        gets the string representable version of input list.

        :param list value: value to get its string representation.

        :returns: string representable value.
        :rtype: list
        """

        if not isinstance(value, LIST_TYPES):
            return self._get_representation(value)

        result = []
        for item in value:
            result.append(self._get_representation(item))

        return result

    @classmethod
    def _get_value(cls, value):
        """
        gets the value of given input.

        it is a helper method which could call the input if
        it is a callable or get the same input.

        :param object | callable value: value to get its original value.
                                        it could be an object or a callable.

        :returns: original value.
        """

        if callable(value):
            return value()

        return value

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

    @property
    def is_list(self):
        """
        gets a value indicating that values must be a list of items.

        :rtype: bool
        """

        return self._is_list

    @property
    def null_items(self):
        """
        gets a value indicating that list items could be None.

        :rtype: bool
        """

        return self._null_items
