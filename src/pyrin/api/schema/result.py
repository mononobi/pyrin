# -*- coding: utf-8 -*-
"""
schema result module.
"""

import pyrin.converters.serializer.services as serializer_services

from pyrin.core.context import CoreObject
from pyrin.api.schema.exceptions import SchemaColumnsOrReplaceIsRequiredError, \
    ColumnNotExistedError, InvalidReplaceKeysError


class ResultSchema(CoreObject):
    """
    result schema class.
    """

    def __init__(self, columns=None, replace=None, **options):
        """
        initializes an instance of ResultSchema.

        note that at least one of `columns` or `replace` must be provided.

        :param list[str] columns: column names to be included in result.

        :param dict replace: a dict containing original column names as
                             keys, and column names that must be exposed
                             instead of original names, as values.
                             for example if `replace = dict(real_name='new_name')`
                             then, the value of `real_name` column in result will
                             be returned as `new_name` column.
                             note that if you provide `columns` input too, then the
                             keys of replace dict must be a subset of `columns`.

        :raises SchemaColumnsOrReplaceIsRequiredError: schema columns or replace
                                                       is required error.

        :raises InvalidReplaceKeysError: invalid replace keys error.
        """

        super().__init__()

        if (columns is None or len(columns) <= 0) and \
                (replace is None or len(replace) <= 0):
            raise SchemaColumnsOrReplaceIsRequiredError('Result schema "columns" or '
                                                        '"replace" must be provided.')

        if columns is None:
            columns = []

        if replace is None:
            replace = {}

        if len(columns) > 0 and len(replace) > 0:
            difference = set(replace.keys()).difference(set(columns))
            if len(difference) > 0:
                raise InvalidReplaceKeysError('"replace" keys {replace} are not present '
                                              'in "columns". when providing both "columns" '
                                              'and "replace" inputs, "replace" keys must '
                                              'be a subset of "columns".'
                                              .format(replace=list(difference)))

        self._columns = columns
        self._replace = replace

    @property
    def columns(self):
        """
        gets the columns attribute of this schema.

        these are the columns that must be returned from the result.

        :rtype: list[str]
        """

        return self._columns

    @property
    def replace(self):
        """
        gets the replace attribute of this schema.

        these are the columns that must be returned
        with modified names from the result.

        :rtype: dict
        """

        return self._replace

    def filter(self, item, **options):
        """
        filters the given item based on current schema.

        if the item is not filterable, it returns the exact input item.

        :param Union[object, list[object]] item: item or items to be filtered.

        :raises ColumnNotExistedError: column not existed error.

        :rtype: Union[dict, list[dict]]
        """

        return self._filter(item, **options)

    def _filter(self, item, **options):
        """
        filters the given item based on current schema.

        if the item is not filterable, it returns the exact input item.

        :param Union[object, list[object]] item: item or items to be filtered.

        :raises ColumnNotExistedError: column not existed error.

        :rtype: Union[dict, list[dict]]
        """

        if item is None:
            return item

        options.pop('columns', None)
        result = serializer_services.serialize(item, columns=self.columns, **options)

        if self._should_filter(result):
            difference = set(self.replace.keys()).difference(set(result.keys()))
            if len(difference) > 0:
                raise ColumnNotExistedError('Columns {columns} are not available in result.'
                                            .format(columns=list(difference)))

            for original_column, new_column in self.replace.items():
                value = result.pop(original_column)
                result[new_column] = value

        return result

    def _is_filterable(self, item):
        """
        gets a value indicating that given item is filterable.

        it actually checks that given item is a dict or a list of dicts
        and dicts have any keys in them. if not, it's not filterable.

        :param Union[object, list[object]] item: item or items to be filtered.

        :rtype: bool
        """

        if isinstance(item, dict) and len(item) > 0:
            return True

        if isinstance(item, list) and len(item) > 0 and \
                isinstance(item[0], dict) and len(item[0]) > 0:
            return True

        return False

    def _should_filter(self, item):
        """
        gets a value indicating that given item should be filtered.

        it actually checks that given item is a dict or a list of dicts
        and dicts have any keys in them and also the `replace` attribute
        of this schema is available. if not, it should not be filtered.

        :param Union[object, list[object]] item: item or items to be checked.

        :rtype: bool
        """

        if self._is_filterable(item) and self._replace is not None and \
                len(self._replace) > 0:
            return True

        return False
