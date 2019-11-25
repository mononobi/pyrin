# -*- coding: utf-8 -*-
"""
utils sqlalchemy module.
"""

from sqlalchemy.orm import lazyload
from sqlalchemy import func
from sqlalchemy.orm import class_mapper, ColumnProperty

import pyrin.utils.datetime as datetime_utils

from pyrin.core.context import DTO
from pyrin.core.exceptions import CoreValueError
from pyrin.core.globals import _, LIST_TYPES


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


def count(query, column=None):
    """
    executes a count query using given query object and returns the result.

    this method generates a sql query like below:
    select count(column)
    from table
    where ...

    you should always use this method instead of sqlalchemy session.query.count()
    because session.query.count() is inefficient.

    :param Query query: sqlalchemy query object.

    :param Column column: column to perform count on it.
                          defaults to `*` if not provided.

    :rtype: int
    """

    func_count = func.count()
    if column is not None:
        func_count = func.count(column)

    statement = query.options(lazyload('*')).statement.with_only_columns(
        [func_count]).order_by(None)

    result = query.session.execute(statement).scalar()

    return result


def add_range_clause(clauses, column, value_lower, value_upper,
                     include_equal_to_lower=True,
                     include_equal_to_upper=True):
    """
    adds range comparison into given clauses using specified inputs.

    :param list clauses: clause list to add range clause to it.
    :param Column column: entity column to add range clause for it.
    :param object value_lower: lower bound of range clause.
    :param object value_upper: upper bound of range clause.

    :param include_equal_to_lower: specifies that lower value
                                   should be considered in range.
                                   defaults to True if not provided.

    :param include_equal_to_upper: specifies that upper value
                                   should be considered in range.
                                   defaults to True if not provided.

    :raises CoreValueError: core value error.
    """

    if value_lower is None and value_upper is None:
        return

    if value_lower is not None and value_upper is not None and value_lower > value_upper:
        raise CoreValueError(_('Invalid range is given.'))

    if value_lower is not None and value_lower == value_upper:
        clauses.append(column == value_lower)
    else:
        if value_lower is not None:
            if include_equal_to_lower is True:
                clauses.append(column >= value_lower)
            else:
                clauses.append(column > value_lower)
        if value_upper is not None:
            if include_equal_to_upper is True:
                clauses.append(column <= value_upper)
            else:
                clauses.append(column < value_upper)


def add_date_range_clause(clauses, column, date_lower, date_upper,
                          include_equal_to_lower=True,
                          include_equal_to_upper=True,
                          **options):
    """
    adds date range comparison into given clauses using specified inputs.

    :param list clauses: clause list to add range clause to it.
    :param Column column: entity column to add range clause for it.
    :param datetime date_lower: lower bound of range clause.
    :param datetime date_upper: upper bound of range clause.

    :param include_equal_to_lower: specifies that lower date
                                   should be considered in range.
                                   defaults to True if not provided.

    :param include_equal_to_upper: specifies that upper date
                                   should be considered in range.
                                   defaults to True if not provided.

    :keyword bool consider_begin_of_day: specifies that consider begin
                                         of day for lower date.
                                         defaults to True if not provided.

    :keyword bool consider_end_of_day: specifies that consider end
                                       of day for upper date.
                                       defaults to True if not provided.

    :raises CoreValueError: core value error.
    """

    consider_begin_of_day = options.get('consider_begin_of_day', True)
    consider_end_of_day = options.get('consider_end_of_day', True)

    if date_lower is not None and consider_begin_of_day is True:
        date_lower = datetime_utils.begin_of_day(date_lower)

    if date_upper is not None and consider_end_of_day is True:
        date_upper = datetime_utils.end_of_day(date_upper)

    add_range_clause(clauses, column, date_lower, date_upper,
                     include_equal_to_lower, include_equal_to_upper)


def add_list_clause(clauses, column, value):
    """
    adds list or single comparison into clauses based on given value.

    :param list clauses: clause list to add comparison clause to it.
    :param Column column: entity column to add comparison clause for it.
    :param Union[object, list[object]] value: value to add comparison for it.
    """

    if value is not None:
        if isinstance(value, LIST_TYPES):
            clauses.append(column.in_(value))
        else:
            clauses.append(column == value)
