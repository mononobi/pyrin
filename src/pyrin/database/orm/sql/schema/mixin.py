# -*- coding: utf-8 -*-
"""
orm sql schema mixin module.
"""

from sqlalchemy import BigInteger, Integer, Sequence

import pyrin.utils.misc as misc_utils
import pyrin.utils.unique_id as uuid_utils

from pyrin.database.orm.types.custom import GUID
from pyrin.database.orm.sql.schema.exceptions import SequenceColumnTypeIsInvalidError


class SequenceColumnMixin:
    """
    sequence column mixin class.
    """

    DEFAULT_CACHE = 100
    DEFAULT_TYPE = BigInteger

    def __init__(self, *args, **kwargs):
        """
        initializes an instance of SequenceColumnMixin.

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

        args = list(args)
        name, type_ = self._extract_name_and_type(args, kwargs)
        if type_ is None:
            type_ = self.DEFAULT_TYPE

        if not misc_utils.is_subclass_or_instance(type_, Integer):
            raise SequenceColumnTypeIsInvalidError('The sequence column type must be an '
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

        kwargs.setdefault('allow_write', False)
        kwargs.setdefault('nullable', False)

        kwargs.update(name=name, type_=type_,
                      autoincrement=False, min_value=1,
                      default=sequence_instance,
                      server_default=sequence_instance.next_value())

        kwargs.pop('onupdate', None)
        kwargs.pop('server_onupdate', None)

        super().__init__(*args, **kwargs)


class GUIDColumnMixin:
    """
    guid column mixin class.
    """

    def __init__(self, *args, **kwargs):
        """
        initializes an instance of GUIDColumnMixin.

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

        args = list(args)
        name, type_ = self._extract_name_and_type(args, kwargs)

        kwargs.setdefault('allow_write', False)
        kwargs.setdefault('nullable', False)

        kwargs.update(name=name, type_=GUID, autoincrement=False,
                      default=uuid_utils.generate_uuid4)

        kwargs.pop('server_default', None)
        kwargs.pop('onupdate', None)
        kwargs.pop('server_onupdate', None)

        super().__init__(*args, **kwargs)


class TypeMixin:
    """
    type mixin class.
    """

    _column_type = None

    def __init__(self, *args, **kwargs):
        """
        initializes an instance of TypeMixin.

        :param str name: the name of this column as represented in the database.
                         this argument may be the first positional argument, or
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

        args = list(args)
        name, type_ = self._extract_name_and_type(args, kwargs)
        kwargs.update(name=name, type_=self._column_type)

        super().__init__(*args, **kwargs)
