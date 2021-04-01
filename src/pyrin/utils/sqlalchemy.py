# -*- coding: utf-8 -*-
"""
utils sqlalchemy module.
"""

from sqlalchemy.sql import quoted_name
from sqlalchemy.engine import result_tuple
from sqlalchemy import inspect as sqla_inspect, Table, text, asc, desc, CheckConstraint

import pyrin.utils.datetime as datetime_utils
import pyrin.utils.string as string_utils

from pyrin.core.globals import _
from pyrin.core.globals import LIST_TYPES
from pyrin.utils.exceptions import InvalidRowResultFieldsAndValuesError, \
    FieldsAndValuesCountMismatchError, CheckConstraintValuesRequiredError, \
    MultipleDeclarativeClassesFoundError, InvalidOrderingColumnError


LIKE_CHAR_COUNT_LIMIT = 20


def like_both(value, start='%', end='%'):
    """
    gets a copy of string with `%` or couple of `_` values attached to both ends.

    it is to be used in like operator.

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
    gets a copy of string with `%` or couple of `_` values attached to beginning.

    it is to be used in like operator.

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
    gets a copy of string with `%` or couple of `_` values attached to end.

    it is to be used in like operator.

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
    processes the value and generates a place holder with count of `_` chars.

    this value could be used in like operator.

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
    gets a copy of string with `count` number of `_` attached to both ends.

    it is to be used in like operator.

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
    gets a copy of string with `count` number of `_` attached to beginning.

    it is to be used in like operator.

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
    gets a copy of string with `count` number of `_` attached to end.

    it is to be used in like operator.

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
                     include_equal_to_upper=True,
                     **options):
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

    if the inputs are date objects, they will be converted to datetime with client
    timezone and `consider_begin_of_day` and `consider_end_of_day` will also
    considered as True.

    :param list clauses: clause list to add datetime range clause to it.
    :param CoreColumn column: entity column to add datetime range clause for it.
    :param datetime | date value_lower: lower bound of datetime range clause.
    :param datetime | date value_upper: upper bound of datetime range clause.

    :param include_equal_to_lower: specifies that lower datetime
                                   should be considered in range.
                                   defaults to True if not provided.

    :param include_equal_to_upper: specifies that upper datetime
                                   should be considered in range.
                                   defaults to True if not provided.

    :keyword bool consider_begin_of_day: specifies that consider begin
                                         of day for lower datetime.
                                         defaults to False if not provided.

    :keyword bool consider_end_of_day: specifies that consider end
                                       of day for upper datetime.
                                       defaults to False if not provided.
    """

    value_lower, value_upper = datetime_utils.normalize_datetime_range(value_lower,
                                                                       value_upper,
                                                                       **options)

    add_range_clause(clauses, column,
                     value_lower, value_upper,
                     include_equal_to_lower,
                     include_equal_to_upper,
                     **options)


def add_comparison_clause(clauses, column, value, **options):
    """
    adds list or single comparison into clauses based on given value.

    if the value type is any of list, tuple or set, it generates an
    `in()` comparison, otherwise it generates a simple `==` comparison.

    :param list clauses: clause list to add comparison clause to it.
    :param CoreColumn column: entity column to add comparison clause for it.
    :param object | list[object] value: value to add comparison for it.
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

    :rtype: ROW_RESULT
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
    result = result_tuple(fields)
    return result(values)


def check_constraint(column, values, **options):
    """
    generates a check constraint for given column and values.

    by default, it generates an `in` check, but this could be changed to
    `not in` by providing `use_in=False` in options.

    if the first item of values is a string, all values will be quoted.

    :param str column: column name to be used in check constraint.
    :param list values: values to be used in check constraint.

    :keyword bool use_in: specifies that it must generate an `in` check.
                          otherwise it generates a `not in` check.
                          defaults to True if not provided.

    :keyword **options: all other keyword arguments will be passed to
                        underlying `CheckConstraint` constructor.

    :raises CheckConstraintValuesRequiredError: check constraint values required error.

    :rtype: CheckConstraint
    """

    if values is None or len(values) <= 0:
        raise CheckConstraintValuesRequiredError('Values for generating a check '
                                                 'constraint must be provided.')

    converter = str
    is_string = isinstance(values[0], str)
    if is_string:
        converter = string_utils.quote
    use_in = options.pop('use_in', True)
    condition = 'in'
    if use_in is False:
        condition = 'not in'

    string_values = ', '.join(converter(item) for item in values)
    sql_text = '{column} {condition} ({values})'.format(column=quoted_name(column, True),
                                                        condition=condition,
                                                        values=string_values)
    options.update(sqltext=sql_text)
    return CheckConstraint(**options)


def range_check_constraint(column, min_value=None, max_value=None, **options):
    """
    generates a range check constraint for given column and values.

    if the values are string, they will be quoted.
    if only one value is provided, a max or min constraint will be generated.

    :param str column: column name to be used in check constraint.
    :param object min_value: min value to be used in check constraint.
    :param object max_value: max value to be used in check constraint.

    :keyword **options: all other keyword arguments will be passed to
                        underlying `CheckConstraint` constructor.

    :raises CheckConstraintValuesRequiredError: check constraint values required error.

    :rtype: CheckConstraint
    """

    if min_value is None and max_value is None:
        raise CheckConstraintValuesRequiredError('Values for generating a range check '
                                                 'constraint must be provided.')

    sql_text = None
    if min_value is not None and max_value is not None:
        sql_text = '{column} >= {min} and {column} <= {max}'
    elif min_value is not None:
        sql_text = '{column} >= {min}'
    else:
        sql_text = '{column} <= {max}'

    if isinstance(min_value, str):
        min_value = string_utils.quote(min_value)

    if isinstance(max_value, str):
        max_value = string_utils.quote(max_value)

    sql_text = sql_text.format(column=quoted_name(column, True),
                               min=min_value, max=max_value)

    options.update(sqltext=sql_text)
    return CheckConstraint(**options)


def get_class_by_table(base, table, **options):
    """
    gets declarative class associated with given table.

    if no class is found this function returns `None`.
    if multiple classes were found (polymorphic cases) additional `data` parameter
    can be given to hint which class to return.

    :param type[BaseEntity] base: declarative base model.
    :param Table table: sqlalchemy table object.

    :keyword dict data: data row to determine the class in polymorphic scenarios.

    :keyword bool raise_multi: specifies that if multiple classes found and
                               also provided data could not help, raise an error.
                               otherwise return None.
                               defaults to True if not provided.

    :note: this code is taken from sqlalchemy-utils project.
    https://github.com/kvesteri/sqlalchemy-utils

    for example:

    class User(CoreEntity):
        _table = 'entity'
        id = AutoPKColumn()
        name = StringColumn()

    get_class_by_table(CoreEntity, User.__table__) -> User class

    this function also supports models using single table inheritance.
    additional data parameter should be provided in these cases.

    for example:

    class Entity(CoreEntity):
        _table = 'entity'
        id = AutoPKColumn()
        name = StringColumn()
        type = StringColumn()
        __mapper_args__ = {
            'polymorphic_on': type,
            'polymorphic_identity': 'entity'
        }

    class User(Entity):
        __mapper_args__ = {
            'polymorphic_identity': 'user'
        }

    get_class_by_table(CoreEntity, Entity.__table__, {'type': 'entity'}) -> Entity class
    get_class_by_table(CoreEntity, Entity.__table__, {'type': 'user'}) -> User class

    it also supports extended entities with unlimited depth, it returns the correct child
    entity.

    for example:

    class EntityBase(CoreEntity):
        _table = 'entity'
        id = AutoPKColumn()

    class Entity2(EntityBase):
        _extend_existing = True
        name = StringColumn()

    class Entity3(Entity2):
        _extend_existing = True
        age = CoreColumn(Integer)

    get_class_by_table(CoreEntity, EntityBase.__table__) -> Entity3 class

    :raises MultipleDeclarativeClassesFoundError: multiple declarative classes found error.

    :returns: declarative class or None.
    :rtype: type[BaseEntity]
    """

    data = options.get('data')
    raise_multi = options.get('raise_multi', True)
    found_classes = []
    for item in base.registry.mappers:
        if len(item.tables) > 0 and item.tables[0] is table:
            found_classes.append(item.entity)

    current_count = len(found_classes)
    temp = list(found_classes)
    if current_count > 1:
        for item in found_classes:
            if item.extend_existing is not True:
                temp.remove(item)

    if current_count > len(temp) > 0:
        found_classes = temp
        if len(found_classes) > 1:
            hierarchies = []
            for item in found_classes:
                hierarchies.append(set(item.__mro__))

            hierarchies = sorted(hierarchies, key=len, reverse=True)
            last = hierarchies[0]
            others = hierarchies[1:]
            union = set().union(*others)
            result = union.symmetric_difference(last)
            if len(result) == 1:
                return result.pop()

        elif len(found_classes) == 1:
            return found_classes[0]

    found_classes = set(found_classes)
    if len(found_classes) > 1:
        if not data:
            if raise_multi is True:
                raise MultipleDeclarativeClassesFoundError('Multiple declarative classes found '
                                                           'for table [{table}]. please provide '
                                                           '"data" parameter for this function '
                                                           'to be able to determine polymorphic '
                                                           'scenarios.'.format(table=table.name))
        else:
            for cls in found_classes:
                mapper = sqla_inspect(cls)
                polymorphic_on = mapper.polymorphic_on.name
                if polymorphic_on in data:
                    if data[polymorphic_on] == mapper.polymorphic_identity:
                        return cls

            if raise_multi is True:
                raise MultipleDeclarativeClassesFoundError('Multiple declarative classes found '
                                                           'for table [{table}]. given data row '
                                                           'does not match any polymorphic '
                                                           'identity of the found classes.'
                                                           .format(table=table.name))
    elif found_classes:
        return found_classes.pop()

    return None


def is_valid_column_name(column):
    """
    gets a value indicating that given column name is valid.

    :param str column: column name.

    :rtype: bool
    """

    if not isinstance(column, str) or len(column) <= 0:
        return False

    column = column.replace('+', '').replace('-', '').strip()
    return len(column) > 0 and ' ' not in column


def get_ordering_info(column):
    """
    gets a tuple containing ordering info for given column name.

    it returns a tuple of two item, first item is column name and
    second item is ordering type which is an `UnaryExpression` from `asc` or `desc`.

    default ordering is ascending, but it could be changed to descending
    by prefixing `-` to column name.

    for example:

    age -> ordering for age column ascending.
    -age -> ordering for age column descending.

    :param str column: column name to get its ordering info.

    :rtype: tuple[str, UnaryExpression]
    """

    order_type = asc
    if column.startswith(('-', '+')):
        if column[0] == '-':
            order_type = desc
        column = column[1:]

    return column, order_type


def get_ordering_criterion(*columns, valid_columns=None, ignore_invalid=True):
    """
    gets required criterion for given columns ordering.

    default ordering is ascending, but it could be changed to descending
    by prefixing `-` to column names.

    this method always ignores empty strings and None values.

    for example:

    name, +age -> ordering for name and age columns both ascending.
    name, -age -> ordering for name ascending and age descending.

    :param str columns: column names to get their ordering criterion.
                        they must be the actual table column names.

    :param list[str] valid_columns: valid column names for ordering.
                                    defaults to None if not provided.
                                    they must be the actual table column
                                    names.

    :param bool ignore_invalid: specifies that if provided columns are
                                not in valid column names, ignore them
                                instead of raising an error. note that
                                this only has effect if `valid_columns`
                                is provided. defaults to True.

    :raises InvalidOrderingColumnError: invalid ordering column error.

    :rtype: tuple[UnaryExpression]
    """

    result = []
    for item in columns:
        if is_valid_column_name(item):
            name, order_type = get_ordering_info(item)
            if valid_columns is None or name in valid_columns:
                result.append(order_type(text(name)))
            elif valid_columns is not None and name not in valid_columns:
                if ignore_invalid is False:
                    raise InvalidOrderingColumnError(_('Column [{name}] is not valid '
                                                       'for ordering.').format(name=name))

    return tuple(result)
