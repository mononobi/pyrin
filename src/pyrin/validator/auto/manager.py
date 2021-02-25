# -*- coding: utf-8 -*-
"""
validator auto manager module.
"""

from uuid import UUID
from decimal import Decimal
from datetime import datetime, date, time

import pyrin.validator.services as validator_services
import pyrin.database.model.services as model_services

from pyrin.core.structs import Manager, Context
from pyrin.validator.auto import ValidatorAutoPackage
from pyrin.validator.auto.handler import AutoValidator
from pyrin.validator.handlers.base import ValidatorBase
from pyrin.validator.handlers.dictionary import DictionaryValidator
from pyrin.validator.handlers.uuid import UUIDValidator
from pyrin.validator.handlers.string import StringValidator
from pyrin.validator.handlers.boolean import BooleanValidator
from pyrin.validator.handlers.datetime import DateTimeValidator, DateValidator, TimeValidator
from pyrin.validator.handlers.number import IntegerValidator, FloatValidator, DecimalValidator
from pyrin.validator.handlers.misc import MaximumValidator, MinimumValidator, \
    RangeValidator, InValidator, NotInValidator


class ValidatorAutoManager(Manager):
    """
    validator auto manager class.
    """

    package_class = ValidatorAutoPackage

    def __init__(self):
        """
        initializes an instance of ValidatorAutoManager.
        """

        super().__init__()

        # a dictionary containing python type to validator map.
        # example: {type | str python_type_or_name: type[AbstractValidatorBase] validator_class}
        self._type_to_validator_map = Context()
        self._initialize_map()

    def _initialize_map(self):
        """
        initializes the python type to validator map.
        """

        self._type_to_validator_map[int] = IntegerValidator
        self._type_to_validator_map[float] = FloatValidator
        self._type_to_validator_map[Decimal] = DecimalValidator
        self._type_to_validator_map[bool] = BooleanValidator
        self._type_to_validator_map[str] = StringValidator
        self._type_to_validator_map[dict] = DictionaryValidator
        self._type_to_validator_map[datetime] = DateTimeValidator
        self._type_to_validator_map[date] = DateValidator
        self._type_to_validator_map[time] = TimeValidator
        self._type_to_validator_map[UUID] = UUIDValidator
        self._type_to_validator_map['max'] = MaximumValidator
        self._type_to_validator_map['min'] = MinimumValidator
        self._type_to_validator_map['range'] = RangeValidator
        self._type_to_validator_map['in'] = InValidator
        self._type_to_validator_map['not_in'] = NotInValidator

    def _get_validator_class(self, python_type):
        """
        gets the validator class for given python type.

        it return None if no validator found with given type or name.

        :param type | str python_type: python type or name of validator class.

        :rtype: type[AbstractValidatorBase]
        """

        return self._type_to_validator_map.get(python_type)

    def _get_type_validator(self, domain, field, **options):
        """
        gets the required type validator for given field.

        :param BaseEntity domain: entity type that this field is related to.
        :param InstrumentedAttribute field: field instance.

        :rtype: AbstractValidatorBase
        """

        collection_type, python_type = field.get_python_type()
        if collection_type is list:
            options.update(is_list=True)

        validator_class = self._get_validator_class(python_type)
        if validator_class is not None:
            return validator_class(domain, field, **options)

        return ValidatorBase(domain, field, **options)

    def _get_range_validator(self, domain, field, **options):
        """
        gets the required range validator for given field.

        it either returns a min validator, max validator, range validator or None.

        :param BaseEntity domain: entity type that this field is related to.
        :param InstrumentedAttribute field: field instance.

        :rtype: AbstractValidatorBase
        """

        validator_class = None
        if field.min_value is not None and field.max_value is not None:
            validator_class = self._get_validator_class('range')

        elif field.min_value is not None:
            validator_class = self._get_validator_class('min')

        elif field.max_value is not None:
            validator_class = self._get_validator_class('max')

        if validator_class is not None:
            return validator_class(domain, field, **options)

        return None

    def _get_in_validator(self, domain, field, **options):
        """
        gets the required in validator for given field.

        it either returns an in validator, not in validator or None.

        :param BaseEntity domain: entity type that this field is related to.
        :param InstrumentedAttribute field: field instance.

        :rtype: AbstractValidatorBase
        """

        validator_class = None
        if field.check_in is not None:
            validator_class = self._get_validator_class('in')

        elif field.check_not_in is not None:
            validator_class = self._get_validator_class('not_in')

        if validator_class is not None:
            return validator_class(domain, field, **options)

        return None

    def register_auto_validator(self, domain, field, **options):
        """
        register required auto validator for given field.

        :param BaseEntity domain: entity type that this field is related to.
        :param InstrumentedAttribute field: field instance.
        """

        type_validator = self._get_type_validator(domain, field, **options)
        range_validator = self._get_range_validator(domain, field, **options)
        in_validator = self._get_in_validator(domain, field, **options)
        custom_validator = validator_services.try_get_validator(domain, field.key)
        if custom_validator is not None:
            options.update(replace=True)

        options.update(type_validator=type_validator,
                       range_validator=range_validator,
                       in_validator=in_validator,
                       custom_validator=custom_validator)

        auto_validator = AutoValidator(domain, field, **options)
        validator_services.register_validator(auto_validator, **options)

    def register_auto_validators(self):
        """
        registers all auto validators.

        it returns the count of registered auto validators.

        :rtype: int
        """

        entities = model_services.get_entities()
        registered = 0
        for entity in entities:
            for column in entity.all_instrumented_attributes:
                if column.validated is True:
                    self.register_auto_validator(entity, column)
                    registered += 1

        return registered
