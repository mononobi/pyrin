# -*- coding: utf-8 -*-
"""
orm sql schema base module.
"""

from uuid import UUID

import sqlalchemy.dialects.mssql as mssql_types
import sqlalchemy.dialects.postgresql as pg_types
import sqlalchemy.dialects.sybase.base as sybase_types

from sqlalchemy.exc import ArgumentError
from sqlalchemy import Column, util, ARRAY

from pyrin.core.globals import LIST_TYPES
from pyrin.utils.sqlalchemy import check_constraint, range_check_constraint
from pyrin.caching.decorators import cached_property
from pyrin.database.orm.sql.operators.base import CoreColumnOperators
from pyrin.database.orm.sql.schema.exceptions import InvalidCheckConstraintError, \
    CheckConstraintConflictError


class CoreColumn(Column, CoreColumnOperators):
    """
    core column class.

    all application models columns must be an instance of this class.
    """

    def __init__(self, *args, **kwargs):
        """
        initializes an instance of CoreColumn.

        :param str name: the name of this column as represented in the database.
                         this argument may be the first positional argument, or
                         specified via keyword.

        :param TypeEngine type_: the column's type, indicated using an instance which
                                 if no arguments are required for the type, the class of
                                 the type can be sent as well.
                                 this argument may be the second positional argument, or
                                 specified via keyword.

        :param object *args: additional positional arguments include various
                             `SchemaItem` derived constructs which will be applied
                             as options to the column.

        :keyword bool autoincrement: set up `auto increment` semantics for an
                                     integer primary key column.

        :keyword callable | object default: a scalar, python callable or `ColumnElement`
                                            expression representing the default value
                                            for this column, which will be invoked upon
                                            insert if this column is otherwise not
                                            specified in the values clause of the insert.

        :keyword str doc: optional string that can be used by the ORM or similar
                          to document attributes on the python side.

        :keyword str key: an optional string identifier which will identify this
                          `Column` object on the `Table`.

        :keyword bool index: when `True`, indicates that the column is indexed.

        :keyword dict info: optional data dictionary which will be populated into the
                            `SchemaItem.info` attribute of this object.

        :keyword bool nullable: when set to `False`, will cause the `Not NULL`
                                phrase to be added when generating ddl for the column.

        :keyword callable | object onupdate: a scalar, python callable, or
                                             `ClauseElement` representing a default
                                             value to be applied to the column within update
                                             statements, which will be invoked upon update
                                             if this column is not present in the set
                                             clause of the update.

        :keyword bool primary_key: if `True`, marks this column as a primary key
                                   column. multiple columns can have this flag set to
                                   specify composite primary keys.

        :keyword str | ClauseElement | TextClause server_default: a `FetchedValue` instance,
                                                                  str, unicode or `text`
                                                                  construct representing the ddl
                                                                  default value for the column.

        :keyword str | ClauseElement | TextClause server_onupdate: a `FetchedValue` instance
                                                                   representing a database-side
                                                                   default generation function,
                                                                   such as a trigger. this
                                                                   indicates to sqlalchemy
                                                                   that a newly generated value
                                                                   will be available after
                                                                   updates. this construct
                                                                   does not actually implement
                                                                   any kind of generation
                                                                   function within the database,
                                                                   which instead must be specified
                                                                   separately.

        :keyword bool quote: force quoting of this column's name on or off,
                             corresponding to `True` or `False`. when left at its default
                             of `None`, the column identifier will be quoted according to
                             whether the name is case sensitive (identifiers with at least one
                             upper case character are treated as case sensitive), or if it's a
                             reserved word.

        :keyword bool unique: when `True`, indicates that this column contains a
                              unique constraint, or if `index` is `True` as well, indicates
                              that the `index` should be created with the unique flag.

        :keyword bool system: when `True`, indicates this is a system column,
                              that is a column which is automatically made available by the
                              database, and should not be included in the columns list for a
                              `create table` statement.

        :keyword str comment: optional string that will render an sql comment
                              on table creation.

        :keyword bool allow_read: specifies that the column should be
                                  included in entity to dict conversion.
                                  defaults to True if not provided.

        :keyword bool allow_write: specifies that the column should be
                                   populated on conversion from dict.
                                   defaults to True if not provided.

        :keyword object | callable min_value: minimum value that this column could have.
                                              it could also be a callable without any inputs.
                                              if a non-callable is provided and the column is
                                              not a primary key and also column name is provided,
                                              it will result in check constraint generation on
                                              database. otherwise it will be ignored and could
                                              be used in validators.
                                              defaults to None if not provided.

        :keyword object | callable max_value: maximum value that this column could have.
                                              it could also be a callable without any inputs.
                                              if a non-callable is provided and the column is
                                              not a primary key and also column name is provided,
                                              it will result in check constraint generation on
                                              database. otherwise it will be ignored and could
                                              be used in validators.
                                              defaults to None if not provided.

        :keyword list | callable check_in: list of valid values for this column.
                                           it could also be a callable without any inputs.
                                           if a non-callable is provided and the column is
                                           not a primary key and also column name is provided,
                                           it will result in check constraint generation on
                                           database. otherwise it will be ignored and could
                                           be used in validators.
                                           defaults to None if not provided.

        :keyword list | callable check_not_in: list of invalid values for this column.
                                               it could also be a callable without any inputs.
                                               if a non-callable is provided and the column is
                                               not a primary key and also column name is provided,
                                               it will result in check constraint generation on
                                               database. otherwise it will be ignored and could
                                               be used in validators.
                                               defaults to None if not provided.

        :note check_in, check_not_in: only one of these options could be provided.
                                      otherwise it raises an error.

        :keyword bool validated: specifies that an automatic validator for this column
                                 must be registered, that is usable through validator
                                 services for create and update.
                                 defaults to False if not provided.

        :keyword bool validated_find: specifies that an automatic find validator for this
                                      column must be registered, that is usable through
                                      validator services for find. defaults to `validated`
                                      value if not provided.

        :keyword bool validated_range: specifies that automatic find range validators for this
                                       column must be registered, that is usable through
                                       validator services for find. defaults to `validated_find`
                                       value if not provided.
                                       note that find range validators are constructed with
                                       names `from_*` and `to_*` for given column if it
                                       is a number or any variant of date and time.
                                       if the type of column is anything else or it is a
                                       primary key, no range validators will be registered
                                       for it and this value will be ignored.
        """

        self.allow_read = kwargs.pop('allow_read', True)
        self.allow_write = kwargs.pop('allow_write', True)
        self.min_value = kwargs.pop('min_value', None)
        self.max_value = kwargs.pop('max_value', None)
        self.check_in = kwargs.pop('check_in', None)
        self.check_not_in = kwargs.pop('check_not_in', None)
        self.validated = kwargs.pop('validated', False)
        self.validated_find = kwargs.pop('validated_find', self.validated)
        self.validated_range = kwargs.pop('validated_range', self.validated_find)

        super().__init__(*args, **kwargs)

    def _get_schema_items(self):
        """
        gets required schema items for this column.

        it will generate required check constraints, sequences and ...

        :raises CheckConstraintConflictError: check constraint conflict error.
        :raises InvalidCheckConstraintError: invalid check constraint error.

        :rtype: list
        """

        custom_items = self._get_custom_schema_items()
        if self.name in (None, '') or self.type is None:
            return custom_items

        if self.primary_key is not True:
            minimum = None
            maximum = None
            if self.min_value is not None and not callable(self.min_value):
                minimum = self.min_value

            if self.max_value is not None and not callable(self.max_value):
                maximum = self.max_value

            if minimum is not None or maximum is not None:
                range_constraint = range_check_constraint(self.name,
                                                          min_value=minimum,
                                                          max_value=maximum)
                custom_items.append(range_constraint)

            if self.check_in is not None and self.check_not_in is not None:
                raise CheckConstraintConflictError('Both "check_in" and "check_not_in" could '
                                                   'not be provided at the same time.')

            is_check_in_callable = callable(self.check_in)
            is_check_not_in_callable = callable(self.check_not_in)
            if self.check_in is not None and not is_check_in_callable \
                    and not (isinstance(self.check_in, LIST_TYPES)
                             and len(self.check_in) > 0):
                raise InvalidCheckConstraintError('Provided value for "check_in" '
                                                  'must be an iterable with at least 1 item.')

            if self.check_not_in is not None and not is_check_not_in_callable \
                    and not (isinstance(self.check_not_in, LIST_TYPES)
                             and len(self.check_not_in) > 0):
                raise InvalidCheckConstraintError('Provided value for "check_not_in" '
                                                  'must be an iterable with at least 1 item.')

            valid_list = None
            invalid_list = None
            if self.check_in is not None and not is_check_in_callable:
                valid_list = self.check_in
            elif self.check_not_in is not None and not is_check_not_in_callable:
                invalid_list = self.check_not_in

            if valid_list is not None:
                constraint = check_constraint(self.name, valid_list)
                custom_items.append(constraint)
            elif invalid_list is not None:
                constraint = check_constraint(self.name, invalid_list, use_in=False)
                custom_items.append(constraint)

        return custom_items

    def _get_custom_schema_items(self):
        """
        gets custom schema items for this column.

        it will generate required check constraints, sequences and ...
        this method is intended to be overridden in subclasses.

        :rtype: list
        """

        return []

    def _init_items(self, *args):
        """
        initializes the list of required items for this column.
        """

        custom_items = self._get_schema_items()
        args = list(args)
        args.extend(custom_items)
        super()._init_items(*args)

    def _real_name(self):
        """
        gets the column's real name.

        :rtype: str
        """

        for column in self.base_columns:
            return column.name

    def _extract_name_and_type(self, args, kwargs):
        """
        extracts name and type parameters from given inputs and removes them from inputs.

        it returns None as each parameter that is not given.
        it is implemented to be used by custom column subclasses.

        :param list args: column positional arguments.
        :param dict kwargs: column keyword arguments.

        :raises ArgumentError: argument error.

        :returns: tuple[str name, CoreColumn type]
        :rtype: tuple[str, CoreColumn]
        """

        name = kwargs.pop('name', None)
        type_ = kwargs.pop('type_', None)
        if len(args) > 0:
            if isinstance(args[0], util.string_types):
                if name is not None:
                    raise ArgumentError('May not pass name positionally and as a keyword.')
                name = args.pop(0)

        if len(args) > 0:
            column_type = args[0]
            if hasattr(column_type, "_sqla_type"):
                if type_ is not None:
                    raise ArgumentError('May not pass type_ positionally and as a keyword.')
                type_ = args.pop(0)

        return name, type_

    def _copy_custom_attributes(self, column):
        """
        copies current column's custom attributes into given column.

        this method is implemented to be able to create valid column
        attributes on copy by sqlalchemy.

        subclasses must override this method and call
        `super()._copy_custom_attributes()` at the end.

        the changes must be done to given column in-place.

        :param CoreColumn column: copied column instance.
        """
        pass

    def get_python_type(self, type_=None):
        """
        gets the python equivalent type of this column's type or given type.

        the returned value is a tuple of two items. first item is the collection
        type if the type is a collection, otherwise its None. the second item is
        the type of values of this column.

        it may return (None, None) if type could not be determined.
        this method is only used on server startup for registering auto validators.

        :param TypeEngine type_: sqlalchemy type instance to get its equivalent python
                                 type. if not provided, the column's type will be used.

        :returns: tuple[type collection_type, type python_type]
        :rtype: tuple[type, type]
        """

        if type_ is None:
            type_ = self.type

        python_type = None
        collection_type = None
        try:
            python_type = type_.python_type
        except (NotImplementedError, AttributeError):
            if isinstance(type_, (mssql_types.BIT, sybase_types.BIT)):
                return None, bool
            if isinstance(type_, (pg_types.UUID,
                                  mssql_types.UNIQUEIDENTIFIER,
                                  sybase_types.UNIQUEIDENTIFIER)):
                return None, UUID

        if python_type is list:
            collection_type = python_type
            python_type = None
            if isinstance(type_, ARRAY) and type_.dimensions == 1:
                __, python_type = self.get_python_type(type_.item_type)

        return collection_type, python_type

    def copy(self, **kw):
        """
        gets a copy of this column.

        this method is overridden to be able to handle custom column attributes correctly.

        :param object kw: extra keyword arguments.

        :rtype: CoreColumn
        """

        column = super().copy(**kw)
        self._copy_custom_attributes(column)

        column.allow_read = self.allow_read
        column.allow_write = self.allow_write
        column.min_value = self.min_value
        column.max_value = self.max_value
        column.check_in = self.check_in
        column.check_not_in = self.check_not_in
        column.validated = self.validated
        column.validated_find = self.validated_find
        column.validated_range = self.validated_range

        return column

    @cached_property
    def fullname(self):
        """
        gets the column's fullname.

        fullname is made up of `table_fullname.column_name`.
        if the column has no table, it only returns the `column_name`.

        :rtype: str
        """

        if self.table is None:
            return self._real_name()

        for single_column in self.table.columns:
            if single_column.name == self.name:
                for base_column in single_column.base_columns:
                    return '{table}.{column}'.format(table=base_column.table.fullname,
                                                     column=self._real_name())

    @property
    def is_foreign_key(self):
        """
        gets a value indicating that this column is a foreign key.

        :rtype: bool
        """

        return len(self.foreign_keys) > 0
