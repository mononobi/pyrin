# -*- coding: utf-8 -*-
"""
range manager module.
"""

from decimal import Decimal
from datetime import datetime, date, time

from pyrin.core.structs import Manager
from pyrin.utilities.range import UtilitiesRangePackage


class RangeManager(Manager):
    """
    range manager class.
    """

    package_class = UtilitiesRangePackage

    # types that support range operations. for example range filtering or range validation.
    RANGE_SUPPORTED_TYPES = (int, float, Decimal, datetime, date, time)

    # keyword prefixes that will be used for range operations.
    # for example range filtering or range validation.
    FROM_KEYWORD_PREFIX = 'from_'
    TO_KEYWORD_PREFIX = 'to_'

    def get_range_filter_names(self, name):
        """
        gets range filter names for given name.

        it returns a tuple of two items. if name is `created_on`, then
        it returns (`from_created_on`, `to_created_on`) as range filters.

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

        columns that are primary keys or their python type is not
        in `RANGE_SUPPORTED_TYPES`, do not support range operations.

        :param sqlalchemy.orm.attributes.InstrumentedAttribute column: column to be checked
                                                                       for range support.

        :rtype: bool
        """

        __, python_type = column.get_python_type()
        return column.primary_key is not True and self.is_range_supported_type(python_type)
