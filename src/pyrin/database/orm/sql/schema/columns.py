# -*- coding: utf-8 -*-
"""
orm sql schema columns module.
"""

import inspect

from sqlalchemy import BigInteger, Integer, Sequence

from pyrin.database.orm.sql.schema.base import CoreColumn
from pyrin.database.orm.sql.schema.exceptions import SequenceColumnTypeIsInvalidError


class PKColumn(CoreColumn):
    """
    pk column class.

    this is a helper class for defining pk columns.
    """

    def __init__(self, *args, **kwargs):
        """
        initializes an instance of PKColumn.

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
                             defaults to True if not provided.

        :keyword dict info: optional data dictionary which will be populated into the
                            `SchemaItem.info` attribute of this object.

        :keyword object server_default: a `FetchedValue` instance, str, unicode
                                        or `text` construct representing the ddl
                                        default value for the column.

        :keyword bool quote: force quoting of this column's name on or off,
                             corresponding to `True` or `False`. when left at its default
                             of `None`, the column identifier will be quoted according to
                             whether the name is case sensitive (identifiers with at least one
                             upper case character are treated as case sensitive), or if it's a
                             reserved word.

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
                                   defaults to False if not provided.
        """

        kwargs.update(nullable=False, primary_key=True)
        kwargs.setdefault('allow_write', False)
        kwargs.setdefault('index', True)
        kwargs.pop('onupdate', None)
        kwargs.pop('server_onupdate', None)
        kwargs.pop('unique', None)

        super().__init__(*args, **kwargs)


class SequencePKColumn(PKColumn):
    """
    sequence pk column class.

    this is a helper class for defining pk columns that gain their value from a sequence.
    it differs from columns that set `autoincrement=True`, because the value of sequence
    columns is available to python side without commit or flush. and also a table can have
    multiple sequence columns which is impossible for auto increment columns.
    """

    DEFAULT_CACHE = 200
    DEFAULT_TYPE = BigInteger

    def __init__(self, sequence_name=None, type_=None, *args, **kwargs):
        """
        initializes an instance of SequencePKColumn.

        :param str sequence_name: sequence name to be generated for this column.
                                  this value is required, but have to set a default
                                  value for it to prevent errors on migrations.

        :param TypeEngine type_: the column's type, indicated using an instance which
                                 if no arguments are required for the type, the class of
                                 the type can be sent as well.
                                 it must be an instance or subclass of `Integer` type.
                                 defaults to `DEFAULT_TYPE` if not provided.

        :param str name: the name of this column as represented in the database.
                         this argument may be the third positional argument, or
                         specified via keyword.

        :param object *args: additional positional arguments include various
                             `SchemaItem` derived constructs which will be applied
                             as options to the column.

        :keyword str doc: optional string that can be used by the ORM or similar
                          to document attributes on the python side.

        :keyword str key: an optional string identifier which will identify this
                          `Column` object on the `Table`.

        :keyword bool index: when `True`, indicates that the column is indexed.
                             defaults to True if not provided.

        :keyword dict info: optional data dictionary which will be populated into the
                            `SchemaItem.info` attribute of this object.

        :keyword bool quote: force quoting of this column's name on or off,
                             corresponding to `True` or `False`. when left at its default
                             of `None`, the column identifier will be quoted according to
                             whether the name is case sensitive (identifiers with at least one
                             upper case character are treated as case sensitive), or if it's a
                             reserved word.

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
                                   defaults to False if not provided.

        :keyword int cache: cache size for sequence.
                            defaults to `DEFAULT_CACHE`, if not provided.
                            to disable cache, you can pass it as None or `0`.

        :raises SequenceColumnTypeIsInvalidError: sequence column type is invalid error.
        """

        if type_ is None:
            type_ = self.DEFAULT_TYPE

        if (inspect.isclass(type_) and not issubclass(type_, Integer)) \
                and not isinstance(type_, Integer):
            raise SequenceColumnTypeIsInvalidError('The sequence column type must be an '
                                                   'instance or subclass of [{integer}].'
                                                   .format(integer=Integer))

        cache = kwargs.pop('cache', self.DEFAULT_CACHE)
        sequence_kwargs = dict()
        if cache is not None and cache > 0:
            sequence_kwargs.update(cache=cache)

        kwargs.update(type_=type_, autoincrement=False,
                      default=Sequence(sequence_name, **sequence_kwargs))

        kwargs.pop('server_default', None)

        super().__init__(*args, **kwargs)
