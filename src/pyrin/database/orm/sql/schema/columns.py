# -*- coding: utf-8 -*-
"""
orm sql schema columns module.
"""

import inspect

from sqlalchemy import BigInteger, Integer, Sequence, ForeignKey

import pyrin.utils.unique_id as uuid_utils

from pyrin.database.orm.types.custom import GUID
from pyrin.database.orm.sql.schema.base import CoreColumn
from pyrin.database.orm.sql.schema.exceptions import SequencePKColumnTypeIsInvalidError, \
    AutoPKColumnTypeIsInvalidError, InvalidFKColumnReferenceTypeError


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


class AutoPKColumn(PKColumn):
    """
    auto pk column class.

    this is a helper class for defining pk columns with auto increment value.
    this type of pk column's value is not available to python side without commit or flush.
    """

    DEFAULT_TYPE = BigInteger

    def __init__(self, *args, **kwargs):
        """
        initializes an instance of AutoPKColumn.

        :param str name: the name of this column as represented in the database.
                         this argument may be the first positional argument, or
                         specified via keyword.

        :param TypeEngine type_: the column's type, indicated using an instance which
                                 if no arguments are required for the type, the class of
                                 the type can be sent as well.
                                 it must be an instance or subclass of `Integer` type.
                                 defaults to `DEFAULT_TYPE` if not provided.
                                 this argument may be the second positional argument, or
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

        :raises AutoPKColumnTypeIsInvalidError: auto pk column type is invalid error.
        """

        args = list(args)
        name, type_ = self._extract_name_and_type(args, kwargs)
        if type_ is None:
            type_ = self.DEFAULT_TYPE

        if (inspect.isclass(type_) and not issubclass(type_, Integer)) \
                and not isinstance(type_, Integer):
            raise AutoPKColumnTypeIsInvalidError('The auto pk column type must be an '
                                                 'instance or subclass of [{integer}].'
                                                 .format(integer=Integer))

        kwargs.update(name=name, type_=type_, autoincrement=True)
        kwargs.pop('default', None)
        kwargs.pop('server_default', None)

        super().__init__(*args, **kwargs)


class GUIDPKColumn(PKColumn):
    """
    guid pk column class.

    this is a helper class for defining pk columns that their value is a guid.
    this type of pk column's value is available to python side without commit or flush.
    """

    def __init__(self, *args, **kwargs):
        """
        initializes an instance of GUIDPKColumn.

        :param str name: the name of this column as represented in the database.
                         this argument may be the first positional argument, or
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
        """

        args = list(args)
        name, type_ = self._extract_name_and_type(args, kwargs)
        kwargs.update(name=name, type_=GUID, autoincrement=False,
                      default=uuid_utils.generate_uuid4)
        kwargs.pop('server_default', None)

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

    def __init__(self, *args, **kwargs):
        """
        initializes an instance of SequencePKColumn.

        :param str name: the name of this column as represented in the database.
                         this argument may be the first positional argument, or
                         specified via keyword.

        :param TypeEngine type_: the column's type, indicated using an instance which
                                 if no arguments are required for the type, the class of
                                 the type can be sent as well.
                                 it must be an instance or subclass of `Integer` type.
                                 defaults to `DEFAULT_TYPE` if not provided.
                                 this argument may be the second positional argument, or
                                 specified via keyword.

        :param object *args: additional positional arguments include various
                             `SchemaItem` derived constructs which will be applied
                             as options to the column.

        :keyword str sequence: sequence name to be generated for this column.
                               this value is required, but has to be set as
                               keyword to prevent errors.

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

        :raises SequencePKColumnTypeIsInvalidError: sequence pk column type is invalid error.
        """

        args = list(args)
        name, type_ = self._extract_name_and_type(args, kwargs)
        if type_ is None:
            type_ = self.DEFAULT_TYPE

        if (inspect.isclass(type_) and not issubclass(type_, Integer)) \
                and not isinstance(type_, Integer):
            raise SequencePKColumnTypeIsInvalidError('The sequence pk column type must be an '
                                                     'instance or subclass of [{integer}].'
                                                     .format(integer=Integer))

        cache = kwargs.pop('cache', self.DEFAULT_CACHE)
        sequence = kwargs.pop('sequence', None)
        sequence_kwargs = dict()
        if cache is not None and cache > 0:
            sequence_kwargs.update(cache=cache)

        sequence_instance = Sequence(sequence, **sequence_kwargs)
        # this is to prevent sqlalchemy errors.
        if sequence is not None:
            args.append(sequence_instance)

        kwargs.update(name=name, type_=type_,
                      autoincrement=False,
                      default=sequence_instance,
                      server_default=sequence_instance.next_value())

        super().__init__(*args, **kwargs)


class FKColumn(CoreColumn):
    """
    fk column class.

    this is a helper class for defining fk columns.
    """

    def __init__(self, *args, **kwargs):
        """
        initializes an instance of FKColumn.

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

        :keyword str | CoreColumn fk: reference column name or instance.
                                      this parameter is required but to
                                      prevent errors it has to be set as keyword.

        :keyword str fk_on_update: optional string. if set, emit ON UPDATE <value> when
                                   issuing DDL for this constraint. typical values include
                                   CASCADE, DELETE and RESTRICT.

        :keyword str fk_on_delete: optional string. if set, emit ON DELETE <value> when
                                   issuing DDL for this constraint. typical values include
                                   CASCADE, DELETE and RESTRICT.

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

        :keyword bool nullable: when set to `False`, will cause the `Not NULL`
                                phrase to be added when generating ddl for the column.
                                default to False if not provided.

        :keyword callable | object onupdate: a scalar, python callable, or
                                             `ClauseElement` representing a default
                                             value to be applied to the column within update
                                             statements, which will be invoked upon update
                                             if this column is not present in the set
                                             clause of the update.

        :keyword bool primary_key: if `True`, marks this column as a primary key
                                   column. multiple columns can have this flag set to
                                   specify composite primary keys.

        :keyword object server_default: a `FetchedValue` instance, str, unicode
                                        or `text` construct representing the ddl
                                        default value for the column.

        :keyword FetchedValue server_onupdate: a `FetchedValue` instance representing a
                                               database-side default generation function,
                                               such as a trigger. this indicates to sqlalchemy
                                               that a newly generated value will be available
                                               after updates. this construct does not actually
                                               implement any kind of generation function within
                                               the database, which instead must be specified
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

        :raises InvalidFKColumnReferenceTypeError: invalid fk column reference type error.
        """

        args = list(args)
        name, type_ = self._extract_name_and_type(args, kwargs)
        fk = kwargs.pop('fk', None)
        fk_on_update = kwargs.pop('fk_on_update', None)
        fk_on_delete = kwargs.pop('fk_on_delete', None)

        if fk is not None and not isinstance(fk, (str, CoreColumn)):
            raise InvalidFKColumnReferenceTypeError('Reference column must be a string '
                                                    'or an instance of [{column}].'
                                                    .format(column=CoreColumn))

        # this is to prevent sqlalchemy errors.
        # because metadata uses uninitialized entities.
        if fk is None:
            fk = ''

        kwargs.update(name=name, type_=type_)
        kwargs.setdefault('index', True)
        kwargs.setdefault('nullable', False)

        super().__init__(ForeignKey(fk, onupdate=fk_on_update, ondelete=fk_on_delete),
                         *args, **kwargs)


class HiddenColumn(CoreColumn):
    """
    hidden column class.

    this is a helper class for defining hidden columns.
    hidden columns will not be included in entity to dict conversion
    and also they won't get populated on conversion from dict.
    """

    def __init__(self, *args, **kwargs):
        """
        initializes an instance of HiddenColumn.

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

        :keyword object server_default: a `FetchedValue` instance, str, unicode
                                        or `text` construct representing the ddl
                                        default value for the column.

        :keyword FetchedValue server_onupdate: a `FetchedValue` instance representing a
                                               database-side default generation function,
                                               such as a trigger. this indicates to sqlalchemy
                                               that a newly generated value will be available
                                               after updates. this construct does not actually
                                               implement any kind of generation function within
                                               the database, which instead must be specified
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
        """

        kwargs.update(allow_read=False)
        kwargs.update(allow_write=False)

        super().__init__(*args, **kwargs)
