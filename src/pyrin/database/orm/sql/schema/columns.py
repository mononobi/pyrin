# -*- coding: utf-8 -*-
"""
orm sql schema columns module.
"""

from sqlalchemy.sql.type_api import Variant
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy import BigInteger, Integer, ForeignKey, String, Unicode, Boolean, \
    SmallInteger, Float, Date, Time, Text, UnicodeText, DECIMAL

import pyrin.utils.misc as misc_utils

from pyrin.database.enumerations import DialectEnum
from pyrin.database.orm.types.custom import CoreDateTime, CoreTimeStamp
from pyrin.database.orm.sql.schema.base import CoreColumn
from pyrin.database.orm.sql.schema.mixin import SequenceColumnMixin, GUIDColumnMixin, TypeMixin
from pyrin.database.orm.sql.schema.exceptions import AutoPKColumnTypeIsInvalidError, \
    InvalidFKColumnReferenceTypeError, StringColumnTypeIsInvalidError, \
    TextColumnTypeIsInvalidError


class StringColumn(CoreColumn):
    """
    string column class.

    this is a helper class to define columns that their type
    is an instance or subclass of sqlalchemy `String`.
    """

    DEFAULT_TYPE = Unicode

    def __init__(self, *args, **kwargs):
        """
        initializes an instance of StringColumn.

        :param str name: the name of this column as represented in the database.
                         this argument may be the first positional argument, or
                         specified via keyword.

        :param TypeEngine type_: the column's type, indicated using an instance which
                                 if no arguments are required for the type, the class of
                                 the type can be sent as well.
                                 this argument may be the second positional argument, or
                                 specified via keyword.
                                 the type must be an instance or subclass of sqlalchemy
                                 `String` type. defaults to `Unicode` if not provided.

        :param object *args: additional positional arguments include various
                             `SchemaItem` derived constructs which will be applied
                             as options to the column.

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

        :keyword int min_length: minimum length of value for this column.
                                 defaults to None if not provided.

        :keyword int max_length: maximum length of value for this column.
                                 if provided, and the type of this column is a
                                 class, it will be instantiated with this length.
                                 defaults to None if not provided.

        :keyword bool allow_blank: specifies that this column could have blank string
                                   value. defaults to False if not provided.

        :keyword bool allow_whitespace: specifies that this column could have whitespace
                                        string value. defaults to False if not provided.

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

        :raises StringColumnTypeIsInvalidError: string column type is invalid error.
        """

        self.min_length = kwargs.pop('min_length', None)
        self.max_length = kwargs.pop('max_length', None)
        self.allow_blank = kwargs.pop('allow_blank', False)
        self.allow_whitespace = kwargs.pop('allow_whitespace', False)

        args = list(args)
        name, type_ = self._extract_name_and_type(args, kwargs)
        if type_ is None:
            type_ = self.DEFAULT_TYPE

        if not misc_utils.is_subclass_or_instance(type_, String):
            raise StringColumnTypeIsInvalidError('The string column type must be '
                                                 'an instance or subclass of [{string}].'
                                                 .format(string=String))

        if isinstance(type_, type) and self.max_length is not None:
            type_ = type_(length=self.max_length)

        kwargs.update(name=name, type_=type_)

        super().__init__(*args, **kwargs)

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

        column.min_length = self.min_length
        column.max_length = self.max_length
        column.allow_blank = self.allow_blank
        column.allow_whitespace = self.allow_whitespace

        super()._copy_custom_attributes(column)


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

        :keyword str | ClauseElement | TextClause server_default: a `FetchedValue` instance,
                                                                  str, unicode or `text`
                                                                  construct representing the ddl
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

        :keyword bool validated: specifies that an automatic validator for this column
                                 must be registered, that is usable through validator
                                 services for create and update.
                                 defaults to False if not provided.

        :keyword bool validated_find: specifies that an automatic find validator for this
                                      column must be registered, that is usable through
                                      validator services for find. defaults to `validated`
                                      value if not provided.
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
    this type of columns handle autoincrement correctly also on sqlite backend.
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

        :keyword bool validated: specifies that an automatic validator for this column
                                 must be registered, that is usable through validator
                                 services for create and update.
                                 defaults to False if not provided.

        :keyword bool validated_find: specifies that an automatic find validator for this
                                      column must be registered, that is usable through
                                      validator services for find. defaults to `validated`
                                      value if not provided.

        :raises AutoPKColumnTypeIsInvalidError: auto pk column type is invalid error.
        """

        args = list(args)
        name, type_ = self._extract_name_and_type(args, kwargs)
        if type_ is None:
            type_ = self.DEFAULT_TYPE

        is_variant = isinstance(type_, Variant)
        if not misc_utils.is_subclass_or_instance(type_, Integer) and \
                not (is_variant and misc_utils.is_subclass_or_instance(type_.impl, Integer)):

            raise AutoPKColumnTypeIsInvalidError('The auto pk column type must be an '
                                                 'instance or subclass of [{integer}].'
                                                 .format(integer=Integer))

        if not is_variant and isinstance(type_, type):
            type_ = type_()

        # this is for sqlite to handle autoincrement correctly also on other
        # variants of Integer. such as BigInteger and SmallInteger.
        if not is_variant:
            type_ = type_.with_variant(Integer, DialectEnum.SQLITE)

        kwargs.update(name=name, type_=type_, autoincrement=True, min_value=1)
        kwargs.pop('default', None)
        kwargs.pop('server_default', None)

        super().__init__(*args, **kwargs)


class GUIDPKColumn(GUIDColumnMixin, PKColumn):
    """
    guid pk column class.

    this is a helper class for defining pk columns that their value is a guid.
    this type of pk column's value is available to python side without commit or flush.
    """
    pass


class SequencePKColumn(SequenceColumnMixin, PKColumn):
    """
    sequence pk column class.

    this is a helper class for defining pk columns that gain their value from a sequence.
    it differs from columns that set `autoincrement=True`, because the value of sequence
    columns is available to python side without commit or flush. and also a table can have
    multiple sequence columns which is impossible for auto increment columns.
    """
    pass


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

        self._fk = kwargs.pop('fk', None)
        self._fk_on_update = kwargs.pop('fk_on_update', None)
        self._fk_on_delete = kwargs.pop('fk_on_delete', None)

        kwargs.setdefault('index', True)
        kwargs.setdefault('nullable', False)

        super().__init__(*args, **kwargs)

    def _get_custom_schema_items(self):
        """
        gets custom schema items for this column.

        it will generate required fk constraint.

        :raises InvalidFKColumnReferenceTypeError: invalid fk column reference type error.

        :rtype: list
        """

        if self._fk is not None and not isinstance(self._fk, (str,
                                                              InstrumentedAttribute,
                                                              CoreColumn)):
            raise InvalidFKColumnReferenceTypeError('Foreign key reference column '
                                                    'must be a string or a column instance.')

        # this is to prevent sqlalchemy errors.
        # because metadata uses uninitialized entities.
        if self._fk is None:
            self._fk = ''

        return [ForeignKey(self._fk,
                           onupdate=self._fk_on_update,
                           ondelete=self._fk_on_delete)]

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

        column._fk = self._fk
        column._fk_on_update = self._fk_on_update
        column._fk_on_delete = self._fk_on_delete

        super()._copy_custom_attributes(column)


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

        kwargs.update(allow_read=False)
        kwargs.update(allow_write=False)

        super().__init__(*args, **kwargs)


class SequenceColumn(SequenceColumnMixin, CoreColumn):
    """
    sequence column class.

    this is a helper class for defining columns which gain their value from a sequence.
    a table can have multiple sequence columns.
    """

    def __init__(self, *args, **kwargs):
        """
        initializes an instance of SequenceColumn.

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

        :keyword str sequence: sequence name to be generated for this column.
                               this value is required, but has to be set as
                               keyword to prevent errors.

        :keyword str doc: optional string that can be used by the ORM or similar
                          to document attributes on the python side.

        :keyword str key: an optional string identifier which will identify this
                          `Column` object on the `Table`.

        :keyword bool index: when `True`, indicates that the column is indexed.

        :keyword dict info: optional data dictionary which will be populated into the
                            `SchemaItem.info` attribute of this object.

        :keyword bool nullable: when set to `False`, will cause the `Not NULL`
                                phrase to be added when generating ddl for the column.
                                defaults to False if not provided.

        :keyword bool primary_key: if `True`, marks this column as a primary key
                                   column. multiple columns can have this flag set to
                                   specify composite primary keys.

        :keyword bool quote: force quoting of this column's name on or off,
                             corresponding to `True` or `False`. when left at its default
                             of `None`, the column identifier will be quoted according to
                             whether the name is case sensitive (identifiers with at least one
                             upper case character are treated as case sensitive), or if it's a
                             reserved word.

        :keyword bool unique: when `True`, indicates that this column contains a
                              unique constraint, or if `index` is `True` as well, indicates
                              that the `index` should be created with the unique flag.
                              defaults to True if not provided.

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

        :keyword int cache: cache size for sequence.
                            defaults to `DEFAULT_CACHE`, if not provided.
                            to disable cache, you can pass it as None or `0`.
                            note that cache is per session, so if you stop the
                            connection to database and start it again, the new
                            session will get its own cache. but it's good for
                            performance to have cache on sequences, gaps are not
                            bad at all.

        :raises SequenceColumnTypeIsInvalidError: sequence column type is invalid error.
        """

        kwargs.setdefault('unique', True)

        super().__init__(*args, **kwargs)


class GUIDColumn(GUIDColumnMixin, CoreColumn):
    """
    guid column class.

    this is a helper class for defining columns which their value is a guid.
    """

    def __init__(self, *args, **kwargs):
        """
        initializes an instance of GUIDColumn.

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

        :keyword dict info: optional data dictionary which will be populated into the
                            `SchemaItem.info` attribute of this object.

        :keyword bool nullable: when set to `False`, will cause the `Not NULL`
                                phrase to be added when generating ddl for the column.
                                defaults to False if not provided.

        :keyword bool primary_key: if `True`, marks this column as a primary key
                                   column. multiple columns can have this flag set to
                                   specify composite primary keys.

        :keyword bool quote: force quoting of this column's name on or off,
                             corresponding to `True` or `False`. when left at its default
                             of `None`, the column identifier will be quoted according to
                             whether the name is case sensitive (identifiers with at least one
                             upper case character are treated as case sensitive), or if it's a
                             reserved word.

        :keyword bool unique: when `True`, indicates that this column contains a
                              unique constraint, or if `index` is `True` as well, indicates
                              that the `index` should be created with the unique flag.
                              defaults to True if not provided.

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

        :keyword bool validated: specifies that an automatic validator for this column
                                 must be registered, that is usable through validator
                                 services for create and update.
                                 defaults to False if not provided.

        :keyword bool validated_find: specifies that an automatic find validator for this
                                      column must be registered, that is usable through
                                      validator services for find. defaults to `validated`
                                      value if not provided.
        """

        kwargs.setdefault('unique', True)

        super().__init__(*args, **kwargs)


class BooleanColumn(TypeMixin, CoreColumn):
    """
    boolean column class.

    this is a helper class for defining columns which their value is a boolean.
    """

    _column_type = Boolean


class BigIntegerColumn(TypeMixin, CoreColumn):
    """
    big integer column class.

    this is a helper class for defining columns which their value is a big integer.
    """

    _column_type = BigInteger


class IntegerColumn(TypeMixin, CoreColumn):
    """
    integer column class.

    this is a helper class for defining columns which their value is an integer.
    """

    _column_type = Integer


class SmallIntegerColumn(TypeMixin, CoreColumn):
    """
    small integer column class.

    this is a helper class for defining columns which their value is a small integer.
    """

    _column_type = SmallInteger


class FloatColumn(TypeMixin, CoreColumn):
    """
    float column class.

    this is a helper class for defining columns which their value is a float.
    """

    _column_type = Float


class DecimalColumn(TypeMixin, CoreColumn):
    """
    decimal column class.

    this is a helper class for defining columns which their value is a decimal.
    """

    _column_type = DECIMAL


class DateTimeColumn(TypeMixin, CoreColumn):
    """
    datetime column class.

    this is a helper class for defining columns which their value is a datetime.
    """

    def __init__(self, *args, **kwargs):
        """
        initializes an instance of DateTimeColumn.

        :param str name: the name of this column as represented in the database.
                         this argument may be the first positional argument, or
                         specified via keyword.

        :param object *args: additional positional arguments include various
                             `SchemaItem` derived constructs which will be applied
                             as options to the column.

        :keyword bool timezone: specifies that this column is timezone aware.
                                defaults to True if not provided.

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

        timezone = kwargs.pop('timezone', True)
        self._column_type = CoreDateTime(timezone=timezone)

        super().__init__(*args, **kwargs)


class DateColumn(TypeMixin, CoreColumn):
    """
    date column class.

    this is a helper class for defining columns which their value is a date.
    """

    _column_type = Date


class TimeColumn(TypeMixin, CoreColumn):
    """
    time column class.

    this is a helper class for defining columns which their value is a time.
    """

    def __init__(self, *args, **kwargs):
        """
        initializes an instance of TimeColumn.

        :param str name: the name of this column as represented in the database.
                         this argument may be the first positional argument, or
                         specified via keyword.

        :param object *args: additional positional arguments include various
                             `SchemaItem` derived constructs which will be applied
                             as options to the column.

        :keyword bool timezone: specifies that this column is timezone aware.
                                defaults to True if not provided.

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

        timezone = kwargs.pop('timezone', True)
        self._column_type = Time(timezone=timezone)

        super().__init__(*args, **kwargs)


class TimeStampColumn(TypeMixin, CoreColumn):
    """
    timestamp column class.

    this is a helper class for defining columns which their value is a datetime.
    """

    def __init__(self, *args, **kwargs):
        """
        initializes an instance of TimeStampColumn.

        :param str name: the name of this column as represented in the database.
                         this argument may be the first positional argument, or
                         specified via keyword.

        :param object *args: additional positional arguments include various
                             `SchemaItem` derived constructs which will be applied
                             as options to the column.

        :keyword bool timezone: specifies that this column is timezone aware.
                                defaults to True if not provided.

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

        timezone = kwargs.pop('timezone', True)
        self._column_type = CoreTimeStamp(timezone=timezone)

        super().__init__(*args, **kwargs)


class TextColumn(StringColumn):
    """
    text column class.

    this is a helper class to define columns that their type is sqlalchemy `Text`.
    """

    DEFAULT_TYPE = UnicodeText

    def __init__(self, *args, **kwargs):
        """
        initializes an instance of TextColumn.

        :param str name: the name of this column as represented in the database.
                         this argument may be the first positional argument, or
                         specified via keyword.

        :param TypeEngine type_: the column's type, indicated using an instance which
                                 if no arguments are required for the type, the class of
                                 the type can be sent as well.
                                 this argument may be the second positional argument, or
                                 specified via keyword.
                                 the type must be an instance or subclass of sqlalchemy
                                 `Text` type. defaults to `UnicodeText` if not provided.

        :param object *args: additional positional arguments include various
                             `SchemaItem` derived constructs which will be applied
                             as options to the column.

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

        :keyword int min_length: minimum length of value for this column.
                                 defaults to None if not provided.

        :keyword int max_length: maximum length of value for this column.
                                 if provided, and the type of this column is a
                                 class, it will be instantiated with this length.
                                 defaults to None if not provided.

        :keyword bool allow_blank: specifies that this column could have blank string
                                   value. defaults to False if not provided.

        :keyword bool allow_whitespace: specifies that this column could have whitespace
                                        string value. defaults to False if not provided.

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

        :raises TextColumnTypeIsInvalidError: text column type is invalid error.
        """

        args = list(args)
        name, type_ = self._extract_name_and_type(args, kwargs)
        if type_ is None:
            type_ = self.DEFAULT_TYPE

        if not misc_utils.is_subclass_or_instance(type_, Text):
            raise TextColumnTypeIsInvalidError('The text column type must be an '
                                               'instance or subclass of [{text}].'
                                               .format(text=Text))

        kwargs.update(name=name, type_=type_)

        super().__init__(*args, **kwargs)
