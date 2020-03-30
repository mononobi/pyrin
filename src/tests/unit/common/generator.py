# -*- coding: utf-8 -*-
"""
common generator module.
"""

from pyrin.utils.sqlalchemy import create_row_result


def generate_row_results(count, fields, values):
    """
    generates row results with given fields and values and count.

    :param int count: count of generated results.
    :param list[str] fields: field names of results.
    :param list[objects] values: values to be used for all rows.

    :rtype: list[ROW_RESULT]
    """

    result = []
    while count > 0:
        result.append(create_row_result(fields, values))
        count = count - 1

    return result


def generate_entity_results(entity_class, count, **kwargs):
    """
    generates entity results with given entity type using given keyword arguments and count.

    :param type[BaseEntity] entity_class: entity class type to put in result.
    :param int count: count of generated results.

    :rtype: list[BaseEntity]
    """

    result = []
    while count > 0:
        result.append(entity_class(**kwargs))
        count = count - 1

    return result
