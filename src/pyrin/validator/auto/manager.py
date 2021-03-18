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
from pyrin.validator.handlers.datetime import DateTimeValidator, DateValidator, TimeValidator, \
    FromDateTimeValidator, ToDateTimeValidator
from pyrin.validator.handlers.number import IntegerValidator, FloatValidator, DecimalValidator
from pyrin.validator.handlers.misc import MaximumValidator, MinimumValidator, \
    RangeValidator, InValidator, NotInValidator


class ValidatorAutoManager(Manager):
    """
    validator auto manager class.
    """

    package_class = ValidatorAutoPackage

    # keywords that will be used to register find validators.
    FROM_KEYWORD = 'from_'
    TO_KEYWORD = 'to_'

    # list of all types that support find range validators.
    FIND_RANGE_VALIDATOR_TYPES = [int, float, Decimal, datetime, date, time]

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
        self._type_to_validator_map['from_datetime'] = FromDateTimeValidator
        self._type_to_validator_map['to_datetime'] = ToDateTimeValidator
        self._type_to_validator_map['max'] = MaximumValidator
        self._type_to_validator_map['min'] = MinimumValidator
        self._type_to_validator_map['range'] = RangeValidator
        self._type_to_validator_map['in'] = InValidator
        self._type_to_validator_map['not_in'] = NotInValidator

    def _get_validator_class(self, python_type, **options):
        """
        gets the validator class for given python type.

        it return None if no validator found with given type or name.

        :param type | str python_type: python type or name of validator class.

        :keyword bool from_datetime: specifies that if python type is `datetime`,
                                     get the `from_datetime` validator.
                                     if set to False, gets the `to_datetime` validator.
                                     if set to None, gets the `datetime` validator.
                                     defaults to None if not provided.

        :rtype: type[AbstractValidatorBase]
        """

        if python_type is datetime:
            from_datetime = options.get('from_datetime')
            if from_datetime is True:
                python_type = 'from_datetime'
            elif from_datetime is False:
                python_type = 'to_datetime'

        return self._type_to_validator_map.get(python_type)

    def _get_type_validator(self, domain, field, **options):
        """
        gets the required type validator for given field.

        it may return None if `force=False` is given and no validator could be created.

        :param BaseEntity domain: entity type that this field is related to.
        :param InstrumentedAttribute field: field instance.

        :keyword bool for_find: specifies that this validator must only
                                be used on validation for find.
                                defaults to False if not provided.

        :keyword str name: a custom name for this validator.
                           if provided, the name of `field` will be ignored.

        :keyword bool force: specifies that if no validator could be
                             created for given field's type, it must return
                             a base validator for it, otherwise it returns None.
                             defaults to True if not provided.

        :keyword bool from_datetime: specifies that if python type is `datetime`,
                                     get the `from_datetime` validator.
                                     if set to False, gets the `to_datetime` validator.
                                     if set to None, gets the `datetime` validator.
                                     defaults to None if not provided.

        :keyword bool allow_list_for_find: allow value to be list too, on validation
                                           for find. single value is also accepted for
                                           find. if not provided and the field is a
                                           column which has `check_in` set for it,
                                           this will be set to True.

        :rtype: AbstractValidatorBase
        """

        force = options.get('force', True)
        collection_type, python_type = field.get_python_type()
        if collection_type is list:
            options.update(is_list=True)

        validator_class = self._get_validator_class(python_type, **options)
        if validator_class is not None:
            return validator_class(domain, field, **options)

        if force is True:
            return ValidatorBase(domain, field, **options)

        return None

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

    def _get_find_validator(self, domain, field, **options):
        """
        gets the required find validator for given field.

        it will only be used in find validation and will only validate
        type of value if it is not None.

        :param BaseEntity domain: entity type that this field is related to.
        :param InstrumentedAttribute field: field instance.

        :rtype: AbstractValidatorBase
        """

        find_validator = validator_services.try_get_validator(domain, field.key)
        if find_validator is None:
            find_validator = self._get_type_validator(domain, field, for_find=True)

        return find_validator

    def _get_find_range_validators(self, domain, field, **options):
        """
        gets the required find range validators for given field.

        it returns a tuple of all required find range validators.
        it may return an empty tuple if no find range validator should be created.

        find range validators are constructed with names `from_*` and `to_*`.
        they will only be used in find validation and will only validate
        type of value if it is not None.

        not that for primary key columns, no find range validators will be created.

        :param BaseEntity domain: entity type that this field is related to.
        :param InstrumentedAttribute field: field instance.

        :rtype: tuple
        """

        collection_type, python_type = field.get_python_type()
        if field.primary_key is True or python_type not in self.FIND_RANGE_VALIDATOR_TYPES:
            return tuple()

        from_name = '{prefix}{field}'.format(prefix=self.FROM_KEYWORD, field=field.key)
        from_validator = self._get_type_validator(domain, field, name=from_name,
                                                  for_find=True, from_datetime=True,
                                                  allow_list_for_find=False)

        to_name = '{prefix}{field}'.format(prefix=self.TO_KEYWORD, field=field.key)
        to_validator = self._get_type_validator(domain, field, name=to_name,
                                                for_find=True, from_datetime=False,
                                                allow_list_for_find=False)

        return from_validator, to_validator

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

    def register_find_validator(self, domain, field, **options):
        """
        registers required find validator for given field.

        :param BaseEntity domain: entity type that this field is related to.
        :param InstrumentedAttribute field: field instance.
        """

        find_validator = self._get_find_validator(domain, field, **options)
        options.update(for_find=True)
        validator_services.register_validator(find_validator, **options)

    def register_find_range_validators(self, domain, field, **options):
        """
        registers required find range validators for given field.

        it returns the count of registered find range validators.

        :param BaseEntity domain: entity type that this field is related to.
        :param InstrumentedAttribute field: field instance.

        :rtype: int
        """

        registered = 0
        find_range_validators = self._get_find_range_validators(domain, field, **options)
        options.update(for_find=True)
        for item in find_range_validators:
            validator_services.register_validator(item, **options)
            registered += 1

        return registered

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

                if column.validated_find is True:
                    self.register_find_validator(entity, column)
                    registered += 1

                if column.validated_range is True:
                    count = self.register_find_range_validators(entity, column)
                    registered += count

        return registered
