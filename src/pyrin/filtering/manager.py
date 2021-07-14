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

    def _get_column_attribute(self, entity, name):
        """
        gets column attribute with given name from given entity type.

        :param type[pyrin.database.model.base.BaseEntity] entity: entity class type to
                                                                  get it column attribute.
        :param str name: column attribute name.

        :rtype: sqlalchemy.orm.attributes.InstrumentedAttribute
        """

        return getattr(entity, name)

    def filter(self, entity, filters, *ignore, **options):
        """
        gets filtering expressions for given entity type based on given filters.

        :param type[pyrin.database.model.base.BaseEntity] entity: entity class type to
                                                                  be used for filtering.

        :param dict filters: filters to be applied.

        :param sqlalchemy.orm.attributes.InstrumentedAttribute ignore: columns to be ignored
                                                                       from filtering.

        :keyword bool remove: remove all keys that are applied as filter from filters input.
                              defaults to True if not provided.

        :keyword bool readable: specifies that any column or attribute
                                which has `allow_read=False` or its name
                                starts with underscore `_`, should not
                                be included in filtering.
                                defaults to True if not provided.

        :returns: list of expressions for filtering.
        :rtype: list
        """

        readable = options.get('readable', True)
        remove = options.get('remove', True)
        all_columns = None
        if readable is False:
            all_columns = entity.primary_key_columns + \
                          entity.foreign_key_columns + entity.all_columns
        else:
            all_columns = entity.readable_primary_key_columns + \
                entity.readable_foreign_key_columns + entity.readable_columns

        ignore_names = [item.key for item in ignore]
        expressions = []
        for name in all_columns:
            if name not in ignore_names:
                column = self._get_column_attribute(entity, name)
                collection_type, python_type = column.get_python_type()
                if name in filters:
                    value = filters.get(name)
                    if remove is not False:
                        filters.pop(name, None)

                    if python_type is str and not \
                            isinstance(value, LIST_TYPES) and collection_type is None:
                        expressions.append(column.icontains(value))
                    else:
                        sqlalchemy_utils.add_comparison_clause(expressions, column, value)

                if range_services.is_range_supported_column(column):
                    from_name, to_name = range_services.get_range_filter_names(name)
                    if from_name in filters or to_name in filters:
                        from_value = filters.get(from_name)
                        to_value = filters.get(to_name)
                        if remove is not False:
                            filters.pop(from_name, None)
                            filters.pop(to_name, None)

                        if python_type is datetime:
                            sqlalchemy_utils.add_datetime_range_clause(expressions, column,
                                                                       from_value, to_value)
                        else:
                            sqlalchemy_utils.add_range_clause(expressions, column,
                                                              from_value, to_value)

        return expressions
