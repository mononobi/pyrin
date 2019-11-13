# -*- coding: utf-8 -*-
"""
utils misc module.
"""

from pyrin.core.context import DTO
from pyrin.core.exceptions import CoreAttributeError


def set_attributes(instance, **kwargs):
    """
    sets the provided keyword arguments as attributes in given object instance.

    :param CoreObject instance: instance to set attributes for.

    :returns: instance with updated attributes.
    :rtype: CoreObject
    """

    if instance is None:
        return instance

    for name, value in kwargs.items():
        setattr(instance, name, value)

    return instance


def extract_attributes(instance, *attributes):
    """
    extracts all attributes with given names from provided object instance.

    :param CoreObject instance: instance to extract attributes from.
    :param attributes: list of all attribute names that should be extracted.

    :raises CoreAttributeError: core attribute error.

    :returns: dict(str name: object value)
    :rtype: dict
    """

    result = DTO()

    if instance is None:
        return result

    for name in attributes:
        if not hasattr(instance, name):
            raise CoreAttributeError('Object [{object}] has no attribute [{name}].'
                                     .format(object=str(instance), name=name))
        result[name] = getattr(instance, name)

    return result
