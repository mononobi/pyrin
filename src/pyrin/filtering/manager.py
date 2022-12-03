# -*- coding: utf-8 -*-
"""
filtering manager module.

this manager exposes an interface to perform filtering on entities.
the main usage for this type of filtering is in `find` services to reduce the relevant code.
there are some rules that need to be noticed:

1. filtering on single values (non-string) will be performed using `==`.
2. filtering on single values (string) will be performed using `icontains`.
3. filtering on list values will be performed using `in`.
4. filtering on range values will be performed using `>=` and `<=`.
"""

import re

from decimal import Decimal
from datetime import datetime, date, time

from sqlalchemy import func
from sqlalchemy.orm import InstrumentedAttribute

import pyrin.utils.misc as misc_utils
import pyrin.utils.sqlalchemy as sqlalchemy_utils

from pyrin.core.structs import Manager
from pyrin.core.globals import LIST_TYPES
from pyrin.filtering import FilteringPackage


class FilteringManager(Manager):
    """
    filtering manager class.
    """

    package_class = FilteringPackage

    # types that support range operations. for example range filtering or range validation.
    RANGE_SUPPORTED_TYPES = (str, int, float, Decimal, datetime, date, time)

    # keyword prefixes that will be used for range operations.
    # for example range filtering or range validation.
    FROM_KEYWORD_PREFIX = 'from_'
    TO_KEYWORD_PREFIX = 'to_'

    # these regexes will be used to remove prefixes from filter names.
    FROM_REGEX = re.compile(f'^{FROM_KEYWORD_PREFIX}')
    TO_REGEX = re.compile(f'^{TO_KEYWORD_PREFIX}')

    def _is_from_range_filter(self, name):
        """
        gets a value indicating that given name is a `from` range filter name.

        :param str name: filter name.

        :rtype: bool
        """

        return name.startswith(self.FROM_KEYWORD_PREFIX) and name != self.FROM_KEYWORD_PREFIX

    def _is_to_range_filter(self, name):
        """
        gets a value indicating that given name is a `to` range filter name.

        :param str name: filter name.

        :rtype: bool
        """

        return name.startswith(self.TO_KEYWORD_PREFIX) and name != self.TO_KEYWORD_PREFIX

    def _is_range_filter_name(self, name):
        """
        gets a value indicating that given name is a range filter name.

        :param str name: filter name.

        :rtype: bool
        """

        return self._is_from_range_filter(name) or self._is_to_range_filter(name)

    def _get_related_column_name(self, name):
        """
        gets the related column name for given range filter name.

        for example:
        if name='from_age' is provided, the related column name would be `age`.

        from_year => year
        to_year => year
        from_id => id
        register_date => register_date

        note that it may return the same input name as well.

        :param str name: range filter name to get its related column name.

        :rtype: str
        """

        if self._is_from_range_filter(name):
            return re.sub(self.FROM_REGEX, '', name)

        elif self._is_to_range_filter(name):
            return re.sub(self.TO_REGEX, '', name)

        return name

    def _get_related_column(self, name, *scope, **options):
        """
        gets the column with given name from the first entity that has it.

        it returns None if the column name is not available in columns
        or expression level hybrid properties of any provided entities.

        :param str name: column name to be found.

        :param type[pyrin.database.model.base.BaseEntity] scope: entities to search
                                                                 for the column.

        :keyword bool readable: specifies that any column or attribute
                                which has `allow_read=False` or its name
                                starts with underscore `_`, should not
                                be included in filtering.
                                defaults to True if not provided.

        :keyword list[InstrumentedAttribute | hybrid_property] exclude: list of columns
                                                                        to be excluded if
                                                                        have been found.

        :rtype: sqlalchemy.orm.attributes.InstrumentedAttribute |
                sqlalchemy.ext.hybrid.hybrid_property
        """

        exclude = options.get('exclude')
        exclude = misc_utils.make_iterable(exclude)
        readable = options.get('readable', True)
        for entity in scope:
            all_columns = None
            if readable is False:
                all_columns = entity.primary_key_columns + \
                              entity.foreign_key_columns + \
                              entity.all_columns + \
                              entity.expression_level_hybrid_properties
            else:
                all_columns = entity.readable_primary_key_columns + \
                              entity.readable_foreign_key_columns + \
                              entity.readable_columns + \
                              entity.expression_level_hybrid_properties

            if name in all_columns:
                column = entity.get_attribute(name)
                if column not in exclude:
                    return column

        return None

    def _add_expression(self, expressions, column,
                        name, to_be_removed, filters):
        """
        adds the relevant expression for given column into given expressions list.

        :param list expressions: list of expressions to add new expression to it.

        :param InstrumentedAttribute | hybrid_property column: column to add
                                                               expression for it.

        :param str name: relevant column name for filtering.
        :param list[str] to_be_removed: a list to add names to it if they used in expression.
        :param dict filters: filters to be applied.
        """

        is_attribute = isinstance(column, InstrumentedAttribute)
        collection_type = None
        python_type = None
        if is_attribute:
            collection_type, python_type = column.get_python_type()

        if name in filters:
            value = filters.get(name)
            to_be_removed.append(name)
            if not is_attribute and isinstance(value, str):
                expressions.append(func.lower(column).contains(value.lower()))

            elif python_type is str and not isinstance(value, LIST_TYPES) \
                    and collection_type is None:
                expressions.append(column.icontains(str(value)))

            else:
                sqlalchemy_utils.add_comparison_clause(expressions, column, value)

        if is_attribute and self.is_range_supported_column(column):
            from_name, to_name = self.get_range_filter_names(name)
            if from_name in filters or to_name in filters:
                from_value = filters.get(from_name)
                to_value = filters.get(to_name)
                to_be_removed.extend([from_name, to_name])
                if python_type is datetime:
                    sqlalchemy_utils.add_datetime_range_clause(expressions, column,
                                                               from_value, to_value)
                elif python_type is str:
                    sqlalchemy_utils.add_string_range_clause(expressions, column,
                                                             from_value, to_value)
                else:
                    sqlalchemy_utils.add_range_clause(expressions, column,
                                                      from_value, to_value)

    def filter(self, filters, *entity, **options):
        """
        gets filtering expressions for given entity types based on given filters.

        **NOTE:**

        if a filter name is available in both `labeled_filters` and columns of
        entities, the value of `labeled_filters` will be used.

        if a filter name is available in columns of more than one entity, the
        first found entity will be used.

        :param dict filters: filters to be applied.

        :param type[pyrin.database.model.base.BaseEntity] entity: entity class type to
                                                                  be used for filtering.

        :keyword list[InstrumentedAttribute | hybrid_property] ignore: columns to be ignored
                                                                       from filtering. this
                                                                       only has effect on
                                                                       `entity` and will be
                                                                       ignored for
                                                                       `labeled_filters`.

        :keyword bool remove: remove all keys that are applied as filter from filters input.
                              defaults to True if not provided.

        :keyword bool readable: specifies that any column or attribute
                                which has `allow_read=False` or its name
                                starts with underscore `_`, should not
                                be included in filtering.
                                defaults to True if not provided.
                                this only has effect on `entity` and will be
                                ignored for `labeled_filters`.

        :keyword dict labeled_filters: a dict containing all columns that should have
                                       a different filter name than their actual column
                                       name. for example:
                                       {'city_name': CityEntity.name,
                                        'person_name': PersonEntity.name}

        :keyword bool ignore_duplicates: specifies that if multiple labeled filters
                                         point to the same column and have the same value
                                         in provided filters, only add one of them in
                                         where clause. defaults to True if not provided.
                                         the main usage for this is in admin page which
                                         produces inclusive filters dynamically.

        :returns: list of expressions for filtering.
        :rtype: list
        """

        labeled_filters = options.get('labeled_filters') or {}
        ignore_duplicates = options.get('ignore_duplicates', True)
        remove = options.get('remove', True)
        ignore = options.get('ignore')
        ignore = misc_utils.make_iterable(ignore)
        ignore_names = [item.key for item in ignore]
        expressions = []
        to_be_removed = []
        filters_copy = dict(**filters)

        if len(labeled_filters) > 0:
            added = dict()
            for name in filters_copy:
                if name not in to_be_removed:
                    column_name = self._get_related_column_name(name)
                    column = labeled_filters.get(column_name)
                    if column is not None:
                        if ignore_duplicates is True and not self._is_range_filter_name(name):
                            added_values = added.setdefault(column, [])
                            value = filters_copy.get(name)
                            if value in added_values:
                                to_be_removed.append(name)
                                continue
                            else:
                                added_values.append(value)

                        self._add_expression(expressions, column, column_name,
                                             to_be_removed, filters_copy)

            for item in to_be_removed:
                filters_copy.pop(item, None)

        if len(entity) > 0:
            options.update(exclude=list(labeled_filters.values()))
            for name, value in filters_copy.items():
                if name not in to_be_removed:
                    column_name = self._get_related_column_name(name)
                    if column_name not in ignore_names:
                        column = self._get_related_column(column_name, *entity, **options)
                        if column is not None:
                            self._add_expression(expressions, column, column_name,
                                                 to_be_removed, filters_copy)

        if remove is not False:
            for item in to_be_removed:
                filters.pop(item, None)

        return expressions

    def get_range_filter_names(self, name):
        """
        gets range filter names for given name.

        it returns a tuple of two items. if name is `created_at`, then
        it returns (`from_created_at`, `to_created_at`) as range filters.

        :param str name: column name.

        :returns: tuple[str lower_bound_name, str upper_bound_name]
        :rtype: tuple[str, str]
        """

        from_range = '{prefix}{field}'.format(prefix=self.FROM_KEYWORD_PREFIX, field=name)
        to_range = '{prefix}{field}'.format(prefix=self.TO_KEYWORD_PREFIX, field=name)
        return from_range, to_range

    def is_range_supported_type(self, type_):
        """
        gets a value indicating that range operations are supported for given type.

        :param type type_: type to be checked for range support.

        :rtype: bool
        """

        return type_ in self.RANGE_SUPPORTED_TYPES

    def is_range_supported_column(self, column):
        """
        gets a value indicating that range operations are supported for given column.

        columns which their python type is not in `RANGE_SUPPORTED_TYPES`,
        do not support range operations.

        :param sqlalchemy.orm.attributes.InstrumentedAttribute column: column to be checked
                                                                       for range support.

        :rtype: bool
        """

        __, python_type = column.get_python_type()
        return self.is_range_supported_type(python_type)
