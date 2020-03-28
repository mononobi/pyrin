# -*- coding: utf-8 -*-
"""
schema result module.
"""

import pyrin.converters.serializer.services as serializer_services

from pyrin.core.structs import CoreObject
from pyrin.api.schema.exceptions import SchemaAttributesRequiredError


class ResultSchema(CoreObject):
    """
    result schema class.
    """

    def __init__(self, **options):
        """
        initializes an instance of ResultSchema.

        note that at least one of keyword arguments must be provided.

        :keyword bool exposed_only: if set to False, it returns all
                                    columns of the entity as dict.
                                    it will be used only for entity conversion.
                                    if not provided, defaults to True.

        :keyword dict[str, list[str]] | list[str] columns: column names to be included in result.
                                                           it could be a list of column names.
                                                           for example:
                                                           `columns=['id', 'name', 'age']`
                                                           but if you want to include
                                                           relationships, then columns for each
                                                           entity must be provided in a key for
                                                           that entity class name.
                                                           for example if there is `CarEntity` and
                                                           `PersonEntity`, it should be like this:
                                                           `columns=dict(CarEntity=
                                                                         ['id', 'name'],
                                                                         PersonEntity=
                                                                         ['id', 'age'])`
                                                           if provided column names are not
                                                           available in result, an error will
                                                           be raised.

        :note columns: dict[str entity_class_name, list[str column_name]] | list[str column_name]

        :keyword dict[str, dict[str, str]] | dict[str, str] rename: column names that must be
                                                                    renamed in the result.
                                                                    it could be a dict with keys
                                                                    as original column names and
                                                                    values as new column names
                                                                    that should be exposed instead
                                                                    of original column names.
                                                                    for example:
                                                                    `rename=dict(age='new_age',
                                                                                 name='new_name')`
                                                                    but if you want to include
                                                                    relationships, then you must
                                                                    provide a dict containing
                                                                    entity class name as key and
                                                                    for value, another dict
                                                                    containing original column
                                                                    names as keys, and column
                                                                    names that must be exposed
                                                                    instead of original names,
                                                                    as values. for example
                                                                    if there is `CarEntity` and `
                                                                    PersonEntity`, it should be
                                                                    like this:
                                                                    `rename=
                                                                    dict(CarEntity=
                                                                         dict(name='new_name'),
                                                                         PersonEntity=
                                                                         dict(age='new_age')`
                                                                    then, the value of `name`
                                                                    column in result will be
                                                                    returned as `new_name` column.
                                                                    and also value of `age` column
                                                                    in result will be returned as
                                                                    'new_age' column. if provided
                                                                    rename columns are not
                                                                    available in result, they
                                                                    will be ignored.

        :note rename: dict[str entity_class_name, dict[str original_column, str new_column]] |
                      dict[str original_column, str new_column]

        :keyword dict[str, list[str]] | list[str] exclude: column names to be excluded from
                                                           result. it could be a list of column
                                                           names. for example:
                                                           `exclude=['id', 'name', 'age']`
                                                           but if you want to include
                                                           relationships, then columns for each
                                                           entity must be provided in a key for
                                                           that entity class name.
                                                           for example if there is `CarEntity`
                                                           and `PersonEntity`, it should be
                                                           like this:
                                                           `exclude=dict(CarEntity=
                                                                         ['id', 'name'],
                                                                         PersonEntity=
                                                                         ['id', 'age'])`
                                                            if provided excluded columns are not
                                                            available in result, they will be
                                                            ignored.

        :note exclude: dict[str entity_class_name, list[str column_name]] | list[str column_name]

        :keyword int depth: a value indicating the depth for conversion.
                            for example if entity A has a relationship with
                            entity B and there is a list of B in A, if `depth=0`
                            is provided, then just columns of A will be available
                            in result dict, but if `depth=1` is provided, then all
                            B entities in A will also be included in the result dict.
                            actually, `depth` specifies that relationships in an
                            entity should be followed by how much depth.
                            note that, if `columns` is also provided, it is required to
                            specify relationship property names in provided columns.
                            otherwise they won't be included even if `depth` is provided.
                            defaults to `default_depth` value of database config store.
                            please be careful on increasing `depth`, it could fail
                            application if set to higher values. choose it wisely.
                            normally the maximum acceptable `depth` would be 2 or 3.
                            there is a hard limit for max valid `depth` which is set
                            in `ConverterMixin.MAX_DEPTH` class variable. providing higher
                            `depth` value than this limit, will cause an error.
                            it will be used only for entity conversion.

        :raises SchemaAttributesRequiredError: schema attributes required error.
        """

        super().__init__()

        columns = options.get('columns', None)
        rename = options.get('rename', None)
        exclude = options.get('exclude', None)
        depth = options.get('depth', None)
        exposed_only = options.get('exposed_only', None)

        if (columns is None or len(columns) <= 0) and \
                (rename is None or len(rename) <= 0) and \
                (exclude is None or len(exclude) <= 0) and \
                depth is None and exposed_only is None:
            raise SchemaAttributesRequiredError('At least one keyword argument of "{name}"'
                                                'must be provided and have value.'
                                                .format(name=self.get_class_name()))

        self._columns = columns
        self._rename = rename
        self._exclude = exclude
        self._depth = depth
        self._exposed_only = exposed_only

    @property
    def columns(self):
        """
        gets the columns attribute of this schema.

        these are the columns that must be returned from the result for each record.

        :returns: dict[str entity_class_name, list[str column_name]] | list[str column_name]
        :rtype: dict[str, list[str]] | list[str]
        """

        return self._columns

    @property
    def rename(self):
        """
        gets the rename attribute of this schema.

        these are the columns that must be returned
        with modified names from the result for each record.

        :returns: dict[str entity_class_name, dict[str original_column, str new_column]] |
                  dict[str original_column, str new_column]

        :rtype: dict[str, dict[str, str]] | dict[str, str]
        """

        return self._rename

    @property
    def exclude(self):
        """
        gets the exclude attribute of this schema.

        these are the columns that must be excluded from the result for each record.

        :returns: dict[str entity_class_name, list[str column_name]] | list[str column_name]
        :rtype: dict[str, list[str]] | list[str]
        """

        return self._exclude

    @property
    def depth(self):
        """
        gets the depth attribute of this schema.

        this is a value that will be used to convert relationships.
        it will be used only for entity conversion.

        :rtype: int
        """

        return self._depth

    @depth.setter
    def depth(self, value):
        """
        sets the depth attribute of this schema.

        this is a value that will be used to convert relationships.
        it will be used only for entity conversion.

        :param int value: depth value to be set. it should not be higher
                          than `ConverterMixin.MAX_DEPTH` value.
        """

        self._depth = value

    @property
    def exposed_only(self):
        """
        gets the exposed_only attribute of this schema.

        it specifies that just exposed columns of an entity must be
        included in result. it will be used only for entity conversion.

        :rtype: bool
        """

        return self._exposed_only

    @exposed_only.setter
    def exposed_only(self, value):
        """
        sets the exposed_only attribute of this schema.

        it specifies that just exposed columns of an entity must be
        included in result. it will be used only for entity conversion.

        :param bool value: exposed only value to be set.
        """

        self._exposed_only = value

    def filter(self, item, **options):
        """
        filters the given item based on current schema.

        :param object item: item to be filtered.

        :raises ColumnNotExistedError: column not existed error.
        :raises InvalidDepthProvidedError: invalid depth provided error.

        :returns: filtered object
        """

        return self._filter(item, **options)

    def _filter(self, item, **options):
        """
        filters the given item based on current schema.

        :param object item: item to be filtered.

        :raises ColumnNotExistedError: column not existed error.
        :raises InvalidDepthProvidedError: invalid depth provided error.

        :returns: filtered object
        """

        if item is None:
            return item

        options.update(columns=self.columns, rename=self.rename,
                       exclude=self.exclude, depth=self.depth,
                       exposed_only=self.exposed_only)

        return serializer_services.serialize(item, **options)
