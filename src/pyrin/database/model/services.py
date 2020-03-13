# -*- coding: utf-8 -*-
"""
model services module.
"""

from pyrin.application.services import get_component
from pyrin.database.model import ModelPackage


def is_base_entity(value):
    """
    gets a value indicating that input value is an instance of base entity type.

    base entity type by default is `CoreEntity`.
    this method could be used where direct reference to base entity
    type produces an error on server startup.

    :param object value: value to be checked.

    :rtype: bool
    """

    return get_component(ModelPackage.COMPONENT_NAME).is_base_entity(value)


def is_base_keyed_tuple(value):
    """
    gets a value indicating that input value is an instance of base keyed tuple type.

    base keyed tuple type by default is `AbstractKeyedTuple`.
    `AbstractKeyedTuple` objects are those objects that are returned by sqlalchemy
    `Query` with columns or multiple entities.

    :param object value: value to be checked.

    :rtype: bool
    """

    return get_component(ModelPackage.COMPONENT_NAME).is_base_keyed_tuple(value)


def get_base_entity_type():
    """
    gets the application's base entity type.

    base entity type by default is `CoreEntity`.
    this method could be used where direct reference to base entity
    type produces an error on server startup.

    :rtype: type
    """

    return get_component(ModelPackage.COMPONENT_NAME).get_base_entity_type()


def get_base_keyed_tuple_type():
    """
    gets the application's base keyed tuple type.

    base keyed tuple type by default is `AbstractKeyedTuple`.
    `AbstractKeyedTuple` objects are those objects that are returned by sqlalchemy
    `Query` with columns or multiple entities.

    :rtype: type
    """

    return get_component(ModelPackage.COMPONENT_NAME).get_base_keyed_tuple_type()
