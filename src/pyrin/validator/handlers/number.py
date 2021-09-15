# -*- coding: utf-8 -*-
"""
validator handlers number module.
"""

from decimal import Decimal

import pyrin.utils.number as number_utils

from pyrin.core.globals import _
from pyrin.validator.handlers.base import ValidatorBase
from pyrin.validator.handlers.exceptions import ValueIsNotNumberError, \
    ValueIsNotIntegerError, ValueIsNotFloatError, ValueIsNotDecimalError


class NumberValidator(ValidatorBase):
    """
    number validator class.
    """

    invalid_type_error = ValueIsNotNumberError
    invalid_type_message = _('The provided value for [{param_name}] '
                             'must be a number.')

    def __init__(self, domain, field, **options):
        """
        initializes an instance of NumberValidator.

        :param type[BaseEntity] | str domain: the domain in which this validator
                                              must be registered. it could be a
                                              type of a BaseEntity subclass.
                                              if a validator must be registered
                                              independent from any BaseEntity subclass,
                                              the domain could be a unique string name.
                                              note that the provided string name must be
                                              unique at application level.

        :param InstrumentedAttribute | str field: validator field name. it could be a
                                                  string or a column. each validator will
                                                  be registered with its field name in
                                                  corresponding domain. to enable automatic
                                                  validations, the provided field name must
                                                  be the exact name of the parameter which
                                                  this validator will validate. if you pass
                                                  a column attribute, some constraints
                                                  such as `nullable`, `min_length`, `max_length`,
                                                  `min_value`, `max_value`, `allow_blank`,
                                                  `allow_whitespace`, `check_in` and
                                                  `check_not_in` could be extracted
                                                  automatically from that column if not provided
                                                  in inputs.

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

        :keyword bool allow_single: specifies that list validator should also
                                    accept single, non list values.
                                    it is only used if `is_list=True` is provided.
                                    defaults to False if not provided.

        :keyword bool allow_empty_list: specifies that list validators should also
                                        accept empty lists.
                                        it is only used if `is_list=True` is provided.
                                        defaults to False if not provided.

        :keyword str name: a custom name for this validator.
                           if provided, the name of `field` will be ignored.

        :keyword bool for_find: specifies that this validator must only
                                be used on validation for find.
                                defaults to False if not provided.

        :raises ValidatorFieldIsRequiredError: validator field is required error.
        :raises ValidatorNameIsRequiredError: validator name is required error.
        :raises InvalidValidatorDomainError: invalid validator domain error.
        :raises ValidatorFixerMustBeCallable: validator fixer must be callable.
        :raises InvalidValidationExceptionTypeError: invalid validation exception type error.
        """

        options.update(accepted_type=(int, float, Decimal), not_accepted_type=bool)
        super().__init__(domain, field, **options)


class IntegerValidator(ValidatorBase):
    """
    integer validator class.
    """

    invalid_type_error = ValueIsNotIntegerError
    invalid_type_message = _('The provided value for [{param_name}] '
                             'must be an integer.')
    default_fixer = number_utils.coerce_to_int

    def __init__(self, domain, field, **options):
        """
        initializes an instance of IntegerValidator.

        :param type[BaseEntity] | str domain: the domain in which this validator
                                              must be registered. it could be a
                                              type of a BaseEntity subclass.
                                              if a validator must be registered
                                              independent from any BaseEntity subclass,
                                              the domain could be a unique string name.
                                              note that the provided string name must be
                                              unique at application level.

        :param InstrumentedAttribute | str field: validator field name. it could be a
                                                  string or a column. each validator will
                                                  be registered with its field name in
                                                  corresponding domain. to enable automatic
                                                  validations, the provided field name must
                                                  be the exact name of the parameter which
                                                  this validator will validate. if you pass
                                                  a column attribute, some constraints
                                                  such as `nullable`, `min_length`, `max_length`,
                                                  `min_value`, `max_value`, `allow_blank`,
                                                  `allow_whitespace`, `check_in` and
                                                  `check_not_in` could be extracted
                                                  automatically from that column if not provided
                                                  in inputs.

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

        :keyword bool allow_single: specifies that list validator should also
                                    accept single, non list values.
                                    it is only used if `is_list=True` is provided.
                                    defaults to False if not provided.

        :keyword bool allow_empty_list: specifies that list validators should also
                                        accept empty lists.
                                        it is only used if `is_list=True` is provided.
                                        defaults to False if not provided.

        :keyword str name: a custom name for this validator.
                           if provided, the name of `field` will be ignored.

        :keyword bool for_find: specifies that this validator must only
                                be used on validation for find.
                                defaults to False if not provided.

        :raises ValidatorFieldIsRequiredError: validator field is required error.
        :raises ValidatorNameIsRequiredError: validator name is required error.
        :raises InvalidValidatorDomainError: invalid validator domain error.
        :raises ValidatorFixerMustBeCallable: validator fixer must be callable.
        :raises InvalidValidationExceptionTypeError: invalid validation exception type error.
        """

        options.update(accepted_type=int, not_accepted_type=bool)
        super().__init__(domain, field, **options)


class FloatValidator(ValidatorBase):
    """
    float validator class.
    """

    invalid_type_error = ValueIsNotFloatError
    invalid_type_message = _('The provided value for [{param_name}] '
                             'must be a float number.')
    default_fixer = number_utils.coerce_to_float

    def __init__(self, domain, field, **options):
        """
        initializes an instance of FloatValidator.

        :param type[BaseEntity] | str domain: the domain in which this validator
                                              must be registered. it could be a
                                              type of a BaseEntity subclass.
                                              if a validator must be registered
                                              independent from any BaseEntity subclass,
                                              the domain could be a unique string name.
                                              note that the provided string name must be
                                              unique at application level.

        :param InstrumentedAttribute | str field: validator field name. it could be a
                                                  string or a column. each validator will
                                                  be registered with its field name in
                                                  corresponding domain. to enable automatic
                                                  validations, the provided field name must
                                                  be the exact name of the parameter which
                                                  this validator will validate. if you pass
                                                  a column attribute, some constraints
                                                  such as `nullable`, `min_length`, `max_length`,
                                                  `min_value`, `max_value`, `allow_blank`,
                                                  `allow_whitespace`, `check_in` and
                                                  `check_not_in` could be extracted
                                                  automatically from that column if not provided
                                                  in inputs.

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

        :keyword bool allow_single: specifies that list validator should also
                                    accept single, non list values.
                                    it is only used if `is_list=True` is provided.
                                    defaults to False if not provided.

        :keyword bool allow_empty_list: specifies that list validators should also
                                        accept empty lists.
                                        it is only used if `is_list=True` is provided.
                                        defaults to False if not provided.

        :keyword str name: a custom name for this validator.
                           if provided, the name of `field` will be ignored.

        :keyword bool for_find: specifies that this validator must only
                                be used on validation for find.
                                defaults to False if not provided.

        :raises ValidatorFieldIsRequiredError: validator field is required error.
        :raises ValidatorNameIsRequiredError: validator name is required error.
        :raises InvalidValidatorDomainError: invalid validator domain error.
        :raises InvalidNotAcceptedTypeError: invalid not accepted type error.
        :raises ValidatorFixerMustBeCallable: validator fixer must be callable.
        :raises InvalidValidationExceptionTypeError: invalid validation exception type error.
        """

        options.update(accepted_type=float)
        super().__init__(domain, field, **options)


class DecimalValidator(ValidatorBase):
    """
    decimal validator class.
    """

    invalid_type_error = ValueIsNotDecimalError
    invalid_type_message = _('The provided value for [{param_name}] '
                             'must be a decimal number.')
    default_fixer = number_utils.coerce_to_decimal

    def __init__(self, domain, field, **options):
        """
        initializes an instance of DecimalValidator.

        :param type[BaseEntity] | str domain: the domain in which this validator
                                              must be registered. it could be a
                                              type of a BaseEntity subclass.
                                              if a validator must be registered
                                              independent from any BaseEntity subclass,
                                              the domain could be a unique string name.
                                              note that the provided string name must be
                                              unique at application level.

        :param InstrumentedAttribute | str field: validator field name. it could be a
                                                  string or a column. each validator will
                                                  be registered with its field name in
                                                  corresponding domain. to enable automatic
                                                  validations, the provided field name must
                                                  be the exact name of the parameter which
                                                  this validator will validate. if you pass
                                                  a column attribute, some constraints
                                                  such as `nullable`, `min_length`, `max_length`,
                                                  `min_value`, `max_value`, `allow_blank`,
                                                  `allow_whitespace`, `check_in` and
                                                  `check_not_in` could be extracted
                                                  automatically from that column if not provided
                                                  in inputs.

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

        :keyword bool allow_single: specifies that list validator should also
                                    accept single, non list values.
                                    it is only used if `is_list=True` is provided.
                                    defaults to False if not provided.

        :keyword bool allow_empty_list: specifies that list validators should also
                                        accept empty lists.
                                        it is only used if `is_list=True` is provided.
                                        defaults to False if not provided.

        :keyword str name: a custom name for this validator.
                           if provided, the name of `field` will be ignored.

        :keyword bool for_find: specifies that this validator must only
                                be used on validation for find.
                                defaults to False if not provided.

        :raises ValidatorFieldIsRequiredError: validator field is required error.
        :raises ValidatorNameIsRequiredError: validator name is required error.
        :raises InvalidValidatorDomainError: invalid validator domain error.
        :raises InvalidNotAcceptedTypeError: invalid not accepted type error.
        :raises ValidatorFixerMustBeCallable: validator fixer must be callable.
        :raises InvalidValidationExceptionTypeError: invalid validation exception type error.
        """

        options.update(accepted_type=Decimal)
        super().__init__(domain, field, **options)
