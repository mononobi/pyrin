# -*- coding: utf-8 -*-
"""
model schema module.
"""

from sqlalchemy import Column


class CoreColumn(Column):
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

        :param Union[callable, object] default: a scalar, python callable or `ColumnElement`
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

        :param Union[callable, object] onupdate: a scalar, python callable, or
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

        :keyword bool exposed: specifies that the column should be
                               exposed on entity to dict conversion.
                               defaults to True if not provided.
        """

        self.exposed = kwargs.pop('exposed', True)
        super().__init__(*args, **kwargs)
