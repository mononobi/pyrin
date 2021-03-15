# -*- coding: utf-8 -*-
"""
validator auto handler module.
"""

from pyrin.validator.interface import AbstractValidatorBase


class AutoValidator(AbstractValidatorBase):
    """
    auto validator class.
    """

    def __init__(self, domain, field, **options):
        """
        initializes an instance of AutoValidator.

        :param type[BaseEntity] domain: the domain in which this validator
                                        must be registered. it must be a
                                        type of a BaseEntity subclass.

        :param InstrumentedAttribute field: validator field. it must be a
                                            column. each validator will be registered
                                            with its field in corresponding domain.

        :keyword AbstractValidatorBase type_validator: the type validator instance.

        :keyword AbstractValidatorBase range_validator: the range validator instance.
                                                        it is either a range validator,
                                                        max validator, min validator or None.

        :keyword AbstractValidatorBase in_validator: the in validator instance.
                                                     it is either an in validator,
                                                     not in validator or None.

        :keyword AbstractValidatorBase custom_validator: a custom validator to extend
                                                         auto validator behavior.
        """

        super().__init__()

        self._name = field.key
        self._domain = domain
        self._type_validator = options.get('type_validator')
        self._range_validator = options.get('range_validator')
        self._in_validator = options.get('in_validator')
        self._custom_validator = options.get('custom_validator')

    def validate(self, value, **options):
        """
        validates the given value.

        it raises an error if validation fails.
        it returns the same or fixed value.

        :param object | list[object] value: value to be validated.

        :keyword bool for_update: specifies that this field is being
                                  validated for update operation.
                                  defaults to False if not provided.

        :keyword bool for_find: specifies that validation is for find operation.
                                defaults to False if not provided.

        :raises ValidationError: validation error.

        :returns: object | list[object]
        """

        for_find = options.get('for_find', False)
        fixed_value = value
        if self._type_validator is not None:
            fixed_value = self._type_validator.validate(fixed_value, **options)

        if for_find is False:
            if self._range_validator is not None:
                fixed_value = self._range_validator.validate(fixed_value, **options)

            if self._in_validator is not None:
                fixed_value = self._in_validator.validate(fixed_value, **options)

            if self._custom_validator is not None:
                fixed_value = self._custom_validator.validate(fixed_value, **options)

        return fixed_value

    @property
    def name(self):
        """
        gets the name of this validator.

        :rtype: str
        """

        return self._name

    @property
    def domain(self):
        """
        gets the domain of this validator.

        domain is the type of a BaseEntity subclass that
        this validator validates a value of it.

        :rtype: type[BaseEntity]
        """

        return self._domain

    @property
    def for_find(self):
        """
        gets a value indicating that this validator should only be used on validation for find.

        :rtype: bool
        """

        return False
