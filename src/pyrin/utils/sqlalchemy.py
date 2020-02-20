# -*- coding: utf-8 -*-
"""
utils sqlalchemy module.
"""

from sqlalchemy.util import lightweight_named_tuple

import pyrin.utils.datetime as datetime_utils

from pyrin.core.context import DTO
from pyrin.core.globals import LIST_TYPES
from pyrin.utils.exceptions import InvalidRowResultFieldsAndValuesError, \
    FieldsAndValuesCountMismatchError


LIKE_CHAR_COUNT_LIMIT = 20


def entity_to_dict(entity, exposed_only=True):
    """
    converts the given entity into a dict and returns it.
    the result dict only contains the columns of the entity
    which their `hidden` attribute is set to False.

    :param CoreEntity entity: entity to be converted.

    :param bool exposed_only: if set to False, it returns all
                              columns of the entity as dict.
                              if not provided, defaults to True.
    
    :rtype: dict
    """

    if entity is None:
        return DTO()

    return entity.to_dict(exposed_only)


def dict_to_entity(entity_class, **kwargs):
    """
    converts the given keyword arguments into
    an specified entity and returns it.

    :param type entity_class: the result entity class type.

    :rtype: CoreEntity
    """

    result = entity_class()
    result.from_dict(**kwargs)
    return result


def entity_to_dict_list(entities, exposed_only=True):
    """
    converts the given list of entities into a
    list of dicts and returns the result.

    :param list[CoreEntity] entities: list of entities.

    :param bool exposed_only: if set to False, it returns all
                              columns of the entity as dict.
                              if not provided, defaults to True.

    :returns list[dict]
    :rtype list
    """

    results = []
    if entities is None or len(entities) <= 0:
        return results

    for single_entity in entities:
        results.append(entity_to_dict(single_entity, exposed_only))

    return results


def keyed_tuple_to_dict(value):
    """
    converts the given `AbstractKeyedTuple` object into a dict.

    :param AbstractKeyedTuple value: value to be converted.

    :rtype: dict
    """

    if value is None or len(value) <= 0:
        return DTO()

    return DTO(zip(value.keys(), value))


def keyed_tuple_to_dict_list(values):
    """
    converts the given list of `AbstractKeyedTuple` objects into a list of dicts.

    :param list[AbstractKeyedTuple] values: values to be converted.

    :rtype: dict
    """

    results = []
    if values is None or len(values) <= 0:
        return results

    for single_value in values:
        results.append(keyed_tuple_to_dict(single_value))

    return results


def like_both(value, start='%', end='%'):
    """
    gets a copy of string with `%` or couple of `_` values
    attached to both ends of it to use in like operator.
    this method is intended to be used as callable for
    sqlalchemy operator methods.

    :param str value: value to be processed.

    :param str start: start place holder to be prefixed.
                      it could be `%` or couple of `_` values
                      for exact matching.
                      defaults to `%` if not provided.

    :param str end: end place holder to be appended.
                    it could be `%` or couple of `_` values
                    for exact matching.
                    defaults to `%` if not provided.

    :rtype: str
    """

    if value is None:
        return None

    value = like_prefix(value, start)
    value = like_suffix(value, end)

    return value


def like_prefix(value, start='%'):
    """
    gets a copy of string with `%` or couple of `_` values
    attached to beginning of it to use in like operator.
    this method is intended to be used as callable for
    sqlalchemy operator methods.

    :param str value: value to be processed.

    :param str start: start place holder to be prefixed.
                      it could be `%` or couple of `_` values
                      for exact matching.
                      defaults to `%` if not provided.

    :rtype: str
    """

    if value is None:
        return None

    return '{start}{value}'.format(start=start, value=value)


def like_suffix(value, end='%'):
    """
    gets a copy of string with `%` or couple of `_` values
    attached to end of it to use in like operator.
    this method is intended to be used as callable for
    sqlalchemy operator methods.

    :param str value: value to be processed.

    :param str end: end place holder to be appended.
                    it could be `%` or couple of `_` values
                    for exact matching.
                    defaults to `%` if not provided.

    :rtype: str
    """

    if value is None:
        return None

    return '{value}{end}'.format(value=value, end=end)


def _process_place_holder(value, count):
    """
    processes the value and generates a place holder with count
    of `_` chars. this value could be used in like operator.

    :param str value: value to be processed.
    :param int count: count of `_` chars to be attached.

    :note count: this value has a limit of `LIKE_CHAR_COUNT_LIMIT`, if
                 the provided value goes upper than this limit, a
                 `%` will be attached instead of it. this limit is
                 for security reason.

    :rtype: str
    """

    if value is None:
        return ''

    if count is None or count <= 0:
        return ''

    place_holder = None
    if count > LIKE_CHAR_COUNT_LIMIT:
        place_holder = '%'

    if place_holder is None:
        place_holder = '_' * count

    return place_holder


def like_exact_both(value, count):
    """
    gets a copy of string with `_` attached to both ends of
    it by count of underscores to use in like operator.

    :param str value: value to be processed.
    :param int count: count of `_` chars to be attached.

    :note count: this value has a limit of `LIKE_CHAR_COUNT_LIMIT`, if
                 the provided value goes upper than this limit, a
                 `%` will be attached instead of it. this limit is
                 for security reason.

    :rtype: str
    """

    place_holder = _process_place_holder(value, count)
    return like_both(value, place_holder, place_holder)


def like_exact_prefix(value, count):
    """
    gets a copy of string with `_` attached to beginning of
    it by count of underscores to use in like operator.

    :param str value: value to be processed.
    :param int count: count of `_` chars to be attached.

    :note count: this value has a limit of `LIKE_CHAR_COUNT_LIMIT`, if
                 the provided value goes upper than this limit, a
                 `%` will be attached instead of it. this limit is
                 for security reason.

    :rtype: str
    """

    place_holder = _process_place_holder(value, count)
    return like_prefix(value, place_holder)


def like_exact_suffix(value, count):
    """
    gets a copy of string with `_` attached to end of
    it by count of underscores to use in like operator.

    :param str value: value to be processed.
    :param int count: count of `_` chars to be attached.

    :note count: this value has a limit of `LIKE_CHAR_COUNT_LIMIT`, if
                 the provided value goes upper than this limit, a
                 `%` will be attached instead of it. this limit is
                 for security reason.

    :rtype: str
    """

    place_holder = _process_place_holder(value, count)
    return like_suffix(value, place_holder)


def add_range_clause(clauses, column, value_lower, value_upper,
                     include_equal_to_lower=True,
                     include_equal_to_upper=True):
    """
    adds range comparison into given clauses using specified inputs.

    :param list clauses: clause list to add range clause to it.
    :param CoreColumn column: entity column to add range clause for it.
    :param object value_lower: lower bound of range clause.
    :param object value_upper: upper bound of range clause.

    :param include_equal_to_lower: specifies that lower value
                                   should be considered in range.
                                   defaults to True if not provided.

    :param include_equal_to_upper: specifies that upper value
                                   should be considered in range.
                                   defaults to True if not provided.
    """

    if value_lower is None and value_upper is None:
        return

    # we swap the upper and lower values in case of user mistake.
    if value_lower is not None and value_upper is not None and value_lower > value_upper:
        value_lower, value_upper = value_upper, value_lower

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


def add_datetime_range_clause(clauses, column,
                              value_lower, value_upper,
                              include_equal_to_lower=True,
                              include_equal_to_upper=True,
                              **options):
    """
    adds datetime range comparison into given clauses using specified inputs.

    :param list clauses: clause list to add datetime range clause to it.
    :param CoreColumn column: entity column to add datetime range clause for it.
    :param datetime value_lower: lower bound of datetime range clause.
    :param datetime value_upper: upper bound of datetime range clause.

    :param include_equal_to_lower: specifies that lower datetime
                                   should be considered in range.
                                   defaults to True if not provided.

    :param include_equal_to_upper: specifies that upper datetime
                                   should be considered in range.
                                   defaults to True if not provided.

    :keyword bool consider_begin_of_day: specifies that consider begin
                                         of day for lower datetime.
                                         defaults to True if not provided.

    :keyword bool consider_end_of_day: specifies that consider end
                                       of day for upper datetime.
                                       defaults to True if not provided.
    """

    value_lower, value_upper = datetime_utils.normalize_datetime_range(value_lower,
                                                                       value_upper,
                                                                       **options)

    add_range_clause(clauses, column,
                     value_lower, value_upper,
                     include_equal_to_lower,
                     include_equal_to_upper)


def add_comparison_clause(clauses, column, value):
    """
    adds list or single comparison into clauses based on given value.
    if the value type is any of list, tuple or set, it generates an
    `in()` comparison, otherwise it generates a simple `==` comparison.

    :param list clauses: clause list to add comparison clause to it.
    :param CoreColumn column: entity column to add comparison clause for it.
    :param Union[object, list[object]] value: value to add comparison for it.
    """

    if value is not None:
        if isinstance(value, LIST_TYPES):
            clauses.append(column.in_(value))
        else:
            clauses.append(column == value)


def create_row_result(fields, values):
    """
    creates a row result object with given fields and values.
    this object type is returned by sqlalchemy `Query` when there
    is column names or multiple entities in query.

    :param list[str] fields: field names of the result object.

    :param list[object] values: values to be mapped to fields.
                                they must be in the same order as fields.

    :raises InvalidRowResultFieldsAndValuesError: invalid row result fields
                                                  and values error.

    :raises FieldsAndValuesCountMismatchError: fields and values count mismatch error.

    :rtype: AbstractKeyedTuple
    """

    if fields is None or values is None:
        raise InvalidRowResultFieldsAndValuesError('Input parameters "fields" and '
                                                   '"values" must both be provided, '
                                                   'they could not be None.')

    if len(fields) != len(values):
        raise FieldsAndValuesCountMismatchError('The length of "fields" which is '
                                                '[{fields}] and "values" which is '
                                                '[{values}] does not match.'
                                                .format(fields=len(fields),
                                                        values=len(values)))

    keyed_tuple = lightweight_named_tuple('result', fields)
    result = keyed_tuple(values)

    return result
