# -*- coding: utf-8 -*-
"""
orm sql schema module.
"""

from sqlalchemy import Column

from pyrin.caching.decorators import cached_property
from pyrin.database.orm.sql.operators.base import CoreColumnOperators


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

        :param object *args: additional positional arguments include various
                             `SchemaItem` derived constructs which will be applied
                             as options to the column.

        :param bool autoincrement: set up `auto increment` semantics for an
                                   integer primary key column.

        :param callable | object default: a scalar, python callable or `ColumnElement`
                                          expression representing the default value
                                          for this column, which will be invoked upon
                                          insert if this column is otherwise not
                                          specified in the values clause of the insert.

        :param str doc: optional string that can be used by the ORM or similar
                        to document attributes on the python side.

        :param str key: an optional string identifier which will identify this
                        `Column` object on the `Table`.

        :param bool index: When `True`, indicates that the column is indexed.

        :param dict info: optional data dictionary which will be populated into the
                          `SchemaItem.info` attribute of this object.

        :param bool nullable: when set to `False`, will cause the `Not NULL`
                              phrase to be added when generating ddl for the column.

        :param callable | object onupdate: a scalar, python callable, or
                                           `ClauseElement` representing a default
                                           value to be applied to the column within update
                                           statements, which will be invoked upon update
                                           if this column is not present in the set
                                           clause of the update.

        :param bool primary_key: if `True`, marks this column as a primary key
                                 column. multiple columns can have this flag set to
                                 specify composite primary keys.

        :param object server_default: a `FetchedValue` instance, str, unicode
                                      or `text` construct representing the ddl
                                      default value for the column.

        :param FetchedValue server_onupdate: a `FetchedValue` instance representing a
                                             database-side default generation function,
                                             such as a trigger. this indicates to sqlalchemy
                                             that a newly generated value will be available
                                             after updates. this construct does not actually
                                             implement any kind of generation function within
                                             the database, which instead must be specified
                                             separately.

        :param bool quote: force quoting of this column's name on or off,
                           corresponding to `True` or `False`. when left at its default
                           of `None`, the column identifier will be quoted according to
                           whether the name is case sensitive (identifiers with at least one
                           upper case character are treated as case sensitive), or if it's a
                           reserved word.

        :param bool unique: when `True`, indicates that this column contains a
                            unique constraint, or if `index` is `True` as well, indicates
                            that the `index` should be created with the unique flag.

        :param bool system: when `True`, indicates this is a system column,
                            that is a column which is automatically made available by the
                            database, and should not be included in the columns list for a
                            `create table` statement.

        :param str comment: optional string that will render an sql comment
                            on table creation.

        :keyword bool allow_read: specifies that the column should be
                                  included in entity to dict conversion.
                                  defaults to True if not provided.

        :keyword bool allow_write: specifies that the column should be
                                   populated on conversion from dict.
                                   defaults to True if not provided.
        """

        self.allow_read = kwargs.pop('allow_read', True)
        self.allow_write = kwargs.pop('allow_write', True)

        super().__init__(*args, **kwargs)

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

    def _real_name(self):
        """
        gets the column's real name.

        :rtype: str
        """

        for column in self.base_columns:
            return column.name
