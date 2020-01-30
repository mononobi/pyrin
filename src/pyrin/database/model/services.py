# -*- coding: utf-8 -*-
"""
model services module.
"""

from pyrin.application.services import get_component
from pyrin.database.model import ModelPackage


def is_core_entity(value):
    """
    gets a value indicating that input value is an instance of `CoreEntity`.
    this method could be used where direct reference to `CoreEntity`
    produces an error.

    :param object value: value to be checked.

    :rtype: bool
    """

    return get_component(ModelPackage.COMPONENT_NAME).is_core_entity(value)


def is_abstract_keyed_tuple(value):
    """
    gets a value indicating that input value is an instance
    of `AbstractKeyedTuple`. `AbstractKeyedTuple` objects are
    those objects that are returned by sqlalchemy `Query`
    with columns or multiple entities.

    :param object value: value to be checked.

    :rtype: bool
    """

    return get_component(ModelPackage.COMPONENT_NAME).is_abstract_keyed_tuple(value)
