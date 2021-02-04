# -*- coding: utf-8 -*-
"""
schema result module.
"""

from copy import deepcopy

import pyrin.converters.serializer.services as serializer_services
import pyrin.configuration.services as config_services

from pyrin.core.globals import SECURE_TRUE, SECURE_FALSE
from pyrin.core.structs import CoreObject
from pyrin.api.schema.exceptions import SecureBooleanIsRequiredError, InvalidStartIndexError


class ResultSchema(CoreObject):
    """
    result schema class.
    """

    # these values could be set if you do not want to set them through '__init__' method.
    # read the '__init__' method's docstring for details.
    default_columns = None
    default_rename = None
    default_exclude = None
    default_depth = None
    default_readable = None
    default_indexed = None
    default_index_name = None
    default_start_index = None

    def __init__(self, **options):
        """
        initializes an instance of ResultSchema.

        note that at least one of keyword arguments must be provided.

        :keyword SECURE_TRUE | SECURE_FALSE readable: specifies that any column or attribute
                                                      which has `allow_read=False` or its name
                                                      starts with underscore `_`, should not
                                                      be included in result dict. defaults to
                                                      `SECURE_TRUE` if not provided.
                                                      it will be used only for entity
                                                      conversion.

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
                                                           available in result, they will be
                                                           ignored.

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

        :keyword bool indexed: specifies that list results must
                               include an extra field as row index.
                               the name of the index field and the initial value
                               of index could be provided by `index_name` and
                               `start_index` respectively. `indexed` keyword has
                               only effect if the returning result contains a list
                               of objects.

        :keyword str index_name: name of the extra field to contain
                                 the row index of each result. if not provided
                                 defaults to `row_num` value.

        :keyword int start_index: the initial value of row index. if not
                                  provided, starts from 1.

        :raises SecureBooleanIsRequiredError: secure boolean is required error.
        :raises InvalidStartIndexError: invalid start index error.
        """

        super().__init__()

        columns = options.get('columns') or self.default_columns
        rename = options.get('rename') or self.default_rename
        exclude = options.get('exclude') or self.default_exclude
        depth = options.get('depth')
        readable = options.get('readable') or self.default_readable
        indexed = options.get('indexed')
        index_name = options.get('index_name') or self.default_index_name
        start_index = options.get('start_index')

        if depth is None:
            depth = self.default_depth

        if indexed is None:
            indexed = self.default_indexed

        if start_index is None:
            start_index = self.default_start_index

        self._default_index_name = config_services.get('api', 'schema', 'index_name')
        self._default_start_index = config_services.get('api', 'schema', 'start_index')

        self._columns = columns
        self._rename = rename
        self._exclude = exclude
        self._depth = depth
        self._indexed = indexed

        # set these to None to populate them using respective properties.
        self._readable = None
        self._index_name = None
        self._start_index = None

        # performing this through respective properties to get validations.
        self.readable = readable
        self.index_name = index_name
        self.start_index = start_index

    def _filter(self, item, **options):
        """
        filters the given item based on current schema.

        :param object item: item to be filtered.

        :keyword PaginatorBase paginator: paginator instance if any.
                                          if provided, it will be used to
                                          generate correct row indexes.

        :raises InvalidDepthProvidedError: invalid depth provided error.

        :returns: filtered object
        """

        if item is None:
            return item

        start_index = self.start_index
        paginator = options.get('paginator')
        if paginator is not None:
            start_index = (paginator.current_page
                           * paginator.current_page_size) - (paginator.current_page_size +
                                                             (-self.start_index))

        options.update(columns=self.columns,
                       rename=self.rename,
                       exclude=self.exclude,
                       depth=self.depth,
                       readable=self.readable,
                       indexed=self.indexed,
                       index_name=self.index_name,
                       start_index=start_index,
                       result_schema=self)

        return serializer_services.serialize(item, **options)

    def get_computed_row_columns(self, row, **options):
        """
        gets a dict containing all computed columns to be added to the result.

        this method is intended to be overridden in subclasses.
        note that the result dict should not contain any `BaseEntity` or
        `ROW_RESULT` values, otherwise a max recursion error may occur.

        :param ROW_RESULT row: the actual row result to be processed.

        :rtype: dict
        """

        return {}

    def get_computed_entity_columns(self, entity, **options):
        """
        gets a dict containing all computed columns to be added to the result.

        this method is intended to be overridden in subclasses.
        note that the result dict should not contain any `BaseEntity` or
        `ROW_RESULT` values, otherwise a max recursion error may occur.

        :param BaseEntity entity: the actual entity to be processed.

        :rtype: dict
        """

        return {}

    def copy(self):
        """
        returns a deep copy of this instance

        :rtype: ResultSchema
        """

        return deepcopy(self)

    def filter(self, item, **options):
        """
        filters the given item based on current schema.

        :param object item: item to be filtered.

        :keyword PaginatorBase paginator: paginator instance if any.
                                          if provided, it will be used to
                                          generate correct row indexes.

        :raises InvalidDepthProvidedError: invalid depth provided error.

        :returns: filtered object
        """

        return self._filter(item, **options)

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
    def readable(self):
        """
        gets the readable attribute of this schema.

        it specifies that just readable attributes of an entity must be
        included in result. which are those that have `allow_read=True`
        and their name does not start with underscore `_`.
        it will be used only for entity conversion.

        :rtype: SECURE_TRUE | SECURE_FALSE
        """

        return self._readable

    @readable.setter
    def readable(self, value):
        """
        sets the readable attribute of this schema.

        it specifies that just readable attributes of an entity must be
        included in result. which are those that have `allow_read=True`
        and their name does not start with underscore `_`.
        it will be used only for entity conversion.

        :param SECURE_TRUE | SECURE_FALSE value: readable value to be set.

        :raises SecureBooleanIsRequiredError: secure boolean is required error.
        """

        if value not in (None, SECURE_TRUE, SECURE_FALSE):
            raise SecureBooleanIsRequiredError('The "readable" attribute of [{schema}] must '
                                               'be set to "SECURE_TRUE" or "SECURE_FALSE" but '
                                               'it is currently set to [{current}].'
                                               .format(schema=self, current=value))

        self._readable = value

    @property
    def indexed(self):
        """
        gets the indexed attribute of this schema.

        :rtype: bool
        """

        return self._indexed

    @indexed.setter
    def indexed(self, value):
        """
        sets the indexed attribute of this schema.

        :param bool value: specifies that this schema should return indexed results.
        """

        if value is None:
            value = False

        self._indexed = value

    @property
    def index_name(self):
        """
        gets the index name attribute of this schema.

        :rtype: str
        """

        return self._index_name

    @index_name.setter
    def index_name(self, value):
        """
        sets the index name attribute of this schema.

        :param str value: index field name.
        """

        if value is None:
            value = self._default_index_name

        self._index_name = value

    @property
    def start_index(self):
        """
        gets the start index attribute of this schema.

        :rtype: int
        """

        return self._start_index

    @start_index.setter
    def start_index(self, value):
        """
        sets the start index attribute of this schema.

        :param int value: start index.
        """

        if value is None:
            value = self._default_start_index

        if not isinstance(value, int):
            raise InvalidStartIndexError('The "start_index" attribute of [{schema}] '
                                         'must be set to an integer but it is currently '
                                         'set to [{current}].'
                                         .format(schema=self, current=value))
        self._start_index = value
