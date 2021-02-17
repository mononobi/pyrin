# -*- coding: utf-8 -*-
"""
validator handlers uuid module.
"""

from uuid import UUID

from pyrin.core.globals import _
from pyrin.validator.handlers.base import ValidatorBase
from pyrin.validator.handlers.exceptions import ValueIsNotUUIDError, ValueIsNotUUID4Error


class UUIDValidator(ValidatorBase):
    """
    uuid validator class.
    """

    invalid_type_error = ValueIsNotUUIDError
    invalid_type_message = _('The provided value for [{param_name}] '
                             'must be of uuid type.')

    def __init__(self, domain, name, **options):
        """
        initializes an instance of UUIDValidator.

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

        :raises ValidatorNameIsRequiredError: validator name is required error.
        :raises InvalidValidatorDomainError: invalid validator domain error.
        :raises ValidatorFixerMustBeCallable: validator fixer must be callable.
        :raises InvalidValidationExceptionTypeError: invalid validation exception type error.
        """

        options.update(accepted_type=UUID)
        super().__init__(domain, name, **options)


class UUID4Validator(UUIDValidator):
    """
    uuid4 validator class.
    """

    invalid_type_error = ValueIsNotUUID4Error
    invalid_type_message = _('The provided value for [{param_name}] '
                             'must be of uuid4 type.')

    def _validate(self, value, **options):
        """
        validates the given value.

        it raises an error if validation fails.

        :param UUID value: value to be validated.

        :raises ValidationError: validation error.
        """

        super()._validate(value, **options)

        if value.version != 4:
            raise self.invalid_type_error(self.invalid_type_message.format(
                param_name=self.localized_name))
