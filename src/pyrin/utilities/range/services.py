# -*- coding: utf-8 -*-
"""
range services module.
"""

from pyrin.utilities.range import UtilitiesRangePackage
from pyrin.application.services import get_component


def get_range_filter_names(name):
    """
    gets range filter names for given name.

    it returns a tuple of two items. if name is `created_on`, then
    it returns (`from_created_on`, `to_created_on`) as range filters.

    :param str name: column name.

    :returns: tuple[str lower_bound_name, str upper_bound_name]
    :rtype: tuple[str, str]
    """

    return get_component(UtilitiesRangePackage.COMPONENT_NAME).get_range_filter_names(name)


def is_range_supported_type(type_):
    """
    gets a value indicating that range operations are supported for given type.

    :param type type_: type to be checked for range support.

    :rtype: bool
    """

    return get_component(UtilitiesRangePackage.COMPONENT_NAME).is_range_supported_type(type_)


def is_range_supported_column(column):
    """
    gets a value indicating that range operations are supported for given column.

    columns that are primary keys or their python type is not
    in `RANGE_SUPPORTED_TYPES`, do not support range operations.

    :param sqlalchemy.orm.attributes.InstrumentedAttribute column: column to be checked
                                                                   for range support.

    :rtype: bool
    """

    return get_component(UtilitiesRangePackage.COMPONENT_NAME).is_range_supported_column(column)
