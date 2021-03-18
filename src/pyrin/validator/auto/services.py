# -*- coding: utf-8 -*-
"""
validator auto services module.
"""

from pyrin.application.services import get_component
from pyrin.validator.auto import ValidatorAutoPackage


def register_auto_validator(domain, field, **options):
    """
    register required auto validator for given field.

    :param BaseEntity domain: entity type that this field is related to.
    :param InstrumentedAttribute field: field instance.
    """

    return get_component(ValidatorAutoPackage.COMPONENT_NAME).register_auto_validator(
        domain, field, **options)


def register_find_validator(domain, field, **options):
    """
    registers required find validator for given field.

    :param BaseEntity domain: entity type that this field is related to.
    :param InstrumentedAttribute field: field instance.
    """

    return get_component(ValidatorAutoPackage.COMPONENT_NAME).register_find_validator(
        domain, field, **options)


def register_find_range_validators(domain, field, **options):
    """
    registers required find range validators for given field.

    it returns the count of registered find range validators.

    :param BaseEntity domain: entity type that this field is related to.
    :param InstrumentedAttribute field: field instance.

    :rtype: int
    """

    return get_component(ValidatorAutoPackage.COMPONENT_NAME).register_find_range_validators(
        domain, field, **options)


def register_auto_validators():
    """
    registers all auto validators.

    it returns the count of registered auto validators.

    :rtype: int
    """

    return get_component(ValidatorAutoPackage.COMPONENT_NAME).register_auto_validators()
