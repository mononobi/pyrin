# -*- coding: utf-8 -*-
"""
utils sqlalchemy module.
"""

from sqlalchemy.orm import class_mapper, ColumnProperty

from pyrin.core.context import DTO


def entity_to_dict(entity):
    """
    converts the given entity into a dict and returns it.
    the result dict only contains the columns of the entity.

    :param CoreEntity entity: entity to be converted.
    
    :rtype: dict
    """

    if entity is None:
        return DTO()

    entity_class = type(entity)
    all_columns = [prop.key for prop in class_mapper(entity_class).iterate_properties
                   if isinstance(prop, ColumnProperty)]

    result = DTO()
    for attr in dir(entity):
        if attr in all_columns:
            result[attr] = getattr(entity, attr)

    return result


def dict_to_entity(dict_value, entity_class):
    """
    converts the given dict into an specified entity and returns it.

    :param dict dict_value: dict to be converted.
    :param type entity_class: the result entity class type.

    :rtype: CoreEntity
    """

    result = entity_class()
    if dict_value is None or len(dict_value) == 0:
        return result

    all_columns = [prop.key for prop in class_mapper(entity_class).iterate_properties
                   if isinstance(prop, ColumnProperty)]

    for key in dict_value.keys():
        if key in all_columns:
            setattr(result, key, dict_value[key])

    return result


def like_both(value):
    """
    gets a copy of string with `%` attached to both
    ends of it to use in like operator.

    :param str value: value to be processed.

    :rtype: str
    """

    if value is None:
        value = ''

    return '%{value}%'.format(value=value)


def like_begin(value):
    """
    gets a copy of string with `%` attached to beginning
    of it to use in like operator.

    :param str value: value to be processed.

    :rtype: str
    """

    if value is None:
        value = ''

    return '%{value}'.format(value=value)


def like_end(value):
    """
    gets a copy of string with `%` attached to end
    of it to use in like operator.

    :param str value: value to be processed.

    :rtype: str
    """

    if value is None:
        value = ''

    return '{value}%'.format(value=value)
