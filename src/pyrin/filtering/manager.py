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

* note that on primary key columns, no range filtering will be done.
"""

from datetime import datetime

import pyrin.utils.misc as misc_utils
import pyrin.utils.sqlalchemy as sqlalchemy_utils
import pyrin.utilities.range.services as range_services

from pyrin.core.structs import Manager
from pyrin.filtering import FilteringPackage
from pyrin.core.globals import LIST_TYPES


class FilteringManager(Manager):
    """
    filtering manager class.
    """

    package_class = FilteringPackage

    def _get_related_column(self, name, *scope, **options):
        """
        gets the column with given name from the first entity that has it.

        it returns None if the column name is not available in
        columns of any of provided entities.

        :param str name: column name to be found.

        :param type[pyrin.database.model.base.BaseEntity] scope: entities to search
                                                                 for the column.

        :keyword bool readable: specifies that any column or attribute
                                which has `allow_read=False` or its name
                                starts with underscore `_`, should not
                                be included in filtering.
                                defaults to True if not provided.

        :keyword list[sqlalchemy.orm.attributes.InstrumentedAttribute] exclude: list of columns
                                                                                to be excluded if
                                                                                have been found.

        :rtype: sqlalchemy.orm.attributes.InstrumentedAttribute
        """

        exclude = options.get('exclude')
        exclude = misc_utils.make_iterable(exclude)
        readable = options.get('readable', True)
        for entity in scope:
            all_columns = None
            if readable is False:
                all_columns = entity.primary_key_columns + \
                              entity.foreign_key_columns + entity.all_columns
            else:
                all_columns = entity.readable_primary_key_columns + \
                              entity.readable_foreign_key_columns + entity.readable_columns

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

        :param sqlalchemy.orm.attributes.InstrumentedAttribute column: column to add
                                                                       expression for it.

        :param str name: relevant column name for filtering.
        :param list[str] to_be_removed: a list to add names to it if they used in expression.
        :param dict filters: filters to be applied.
        """

        value = filters.get(name)
        to_be_removed.append(name)
        collection_type, python_type = column.get_python_type()
        if python_type is str and not isinstance(value, LIST_TYPES) \
                and collection_type is None:
            expressions.append(column.icontains(str(value)))
        else:
            sqlalchemy_utils.add_comparison_clause(expressions, column, value)

        if range_services.is_range_supported_column(column):
            from_name, to_name = range_services.get_range_filter_names(name)
            if from_name in filters or to_name in filters:
                from_value = filters.get(from_name)
                to_value = filters.get(to_name)
                to_be_removed.extend([from_name, to_name])
                if python_type is datetime:
                    sqlalchemy_utils.add_datetime_range_clause(expressions, column,
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

        :keyword list[sqlalchemy.orm.attributes.InstrumentedAttribute] ignore: columns to be
                                                                               ignored from
                                                                               filtering. this
                                                                               only has effect
                                                                               on `entity` and
                                                                               will be ignored for
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

        :returns: list of expressions for filtering.
        :rtype: list
        """

        labeled_filters = options.get('labeled_filters') or {}
        remove = options.get('remove', True)
        ignore = options.get('ignore')
        ignore = misc_utils.make_iterable(ignore)
        ignore_names = [item.key for item in ignore]
        expressions = []
        to_be_removed = []
        filters_copy = dict(**filters)

        for name, value in filters_copy.items():
            if name in labeled_filters:
                column = labeled_filters.get(name)
                self._add_expression(expressions, column, name, to_be_removed, filters_copy)

        for item in to_be_removed:
            filters_copy.pop(item, None)

        if len(entity) > 0:
            options.update(exclude=list(labeled_filters.values()))
            for name, value in filters_copy.items():
                if name not in ignore_names:
                    column = self._get_related_column(name, *entity, **options)
                    if column is not None:
                        self._add_expression(expressions, column, name,
                                             to_be_removed, filters_copy)

        if remove is not False:
            for item in to_be_removed:
                filters.pop(item, None)

        return expressions
