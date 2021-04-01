# -*- coding: utf-8 -*-
"""
model mixin module.

this module provides mixin classes for different features of declarative base entity.
if you want to implement a new declarative base class and not use the `CoreEntity`
provided by pyrin, you could define your new base class and it must be inherited
from `BaseEntity`, because application will check isinstance() on `BaseEntity` type
to detect models. and then implement your customized or new features in your base class.
then you must put `metaclass=DeclarativeMeta` on your new base class. now all your concrete
entities must be inherited from the new declarative base class. note that you must use a
unique declarative base class for all your models, do not mix `CoreEntity` and your new
declarative base class usage. otherwise you will face problems in migrations and also
multi-database environments.
"""

import inspect

from abc import abstractmethod

from sqlalchemy import inspect as sqla_inspect, UniqueConstraint
from sqlalchemy.orm import declared_attr
from sqlalchemy.exc import NoInspectionAvailable
from sqlalchemy.ext.hybrid import hybrid_property

import pyrin.globalization.datetime.services as datetime_services
import pyrin.database.model.services as model_services
import pyrin.configuration.services as config_services
import pyrin.utils.sqlalchemy as sqlalchemy_utils
import pyrin.utils.misc as misc_utils

from pyrin.core.globals import _
from pyrin.core.decorators import class_property
from pyrin.caching.mixin.decorators import fast_cache
from pyrin.caching.mixin.typed import TypedCacheMixin
from pyrin.core.globals import LIST_TYPES, SECURE_TRUE, SECURE_FALSE
from pyrin.database.orm.sql.schema.base import CoreColumn
from pyrin.database.orm.sql.schema.columns import TimeStampColumn
from pyrin.utils.custom_print import print_warning
from pyrin.core.exceptions import CoreNotImplementedError
from pyrin.database.services import get_current_store
from pyrin.core.structs import DTO, CoreImmutableDict
from pyrin.utils.exceptions import InvalidOrderingColumnError
from pyrin.database.model.exceptions import ColumnNotExistedError, \
    InvalidDeclarativeBaseTypeError, InvalidDepthProvidedError, InvalidOrderingColumnTypeError


class ModelMixinBase:
    """
    model mixin base class.

    all model mixins that have cached values must be subclassed from this.
    """

    @classmethod
    def populate_cache(cls):
        """
        populates all related caches.

        this method will be get called on server startup for each entity.
        subclasses must call `super().populate_cache()` at the end.
        """
        pass


class ColumnMixin(ModelMixinBase):
    """
    column mixin class.

    this class adds functionalities about columns (other than pk and fk) to its subclasses.
    """

    @class_property
    @fast_cache
    def all_columns(cls):
        """
        gets all column names of this entity.

        note that primary and foreign keys are not included in columns.
        column names will be calculated once and cached.

        note:
        as a column is either readable or not readable, so readable columns and
        not readable columns equal to all columns, as is for writable and
        not writable columns.

        :rtype: tuple[str]
        """

        return cls.readable_columns + cls.not_readable_columns

    @class_property
    @fast_cache
    def readable_columns(cls):
        """
        gets readable column names of this entity.

        which are those that have `allow_read=True` in their definition
        and their name does not start with underscore `_`.
        note that primary and foreign keys are not included in columns.
        column names will be calculated once and cached.

        :rtype: tuple[str]
        """

        info = sqla_inspect(cls)
        columns = tuple(attr.key for attr in info.column_attrs
                        if cls.is_public(attr.key) is True and
                        attr.columns[0].is_foreign_key is False and
                        attr.columns[0].primary_key is False and
                        attr.columns[0].allow_read is True)

        return columns

    @class_property
    @fast_cache
    def not_readable_columns(cls):
        """
        gets not readable column names of this entity.

        which are those that have `allow_read=False` in their definition
        or their name starts with underscore `_`.
        note that primary and foreign keys are not included in columns.
        column names will be calculated once and cached.

        :rtype: tuple[str]
        """

        info = sqla_inspect(cls)
        columns = tuple(attr.key for attr in info.column_attrs
                        if (cls.is_public(attr.key) is False or
                            attr.columns[0].allow_read is False) and
                        attr.columns[0].is_foreign_key is False and
                        attr.columns[0].primary_key is False)

        return columns

    @class_property
    @fast_cache
    def writable_columns(cls):
        """
        gets writable column names of this entity.

        which are those that have `allow_write=True` in their definition
        and their name does not start with underscore `_`.
        note that primary and foreign keys are not included in columns.
        column names will be calculated once and cached.

        :rtype: tuple[str]
        """

        info = sqla_inspect(cls)
        columns = tuple(attr.key for attr in info.column_attrs
                        if cls.is_public(attr.key) is True and
                        attr.columns[0].is_foreign_key is False and
                        attr.columns[0].primary_key is False and
                        attr.columns[0].allow_write is True)

        return columns

    @class_property
    @fast_cache
    def not_writable_columns(cls):
        """
        gets not writable column names of this entity.

        which are those that have `allow_write=False` in their definition
        or their name starts with underscore `_`.
        note that primary and foreign keys are not included in columns.
        column names will be calculated once and cached.

        :rtype: tuple[str]
        """

        info = sqla_inspect(cls)
        columns = tuple(attr.key for attr in info.column_attrs
                        if (cls.is_public(attr.key) is False or
                            attr.columns[0].allow_write is False) and
                        attr.columns[0].is_foreign_key is False and
                        attr.columns[0].primary_key is False)

        return columns

    @classmethod
    def populate_cache(cls):
        """
        populates all related caches.
        """

        temp = cls.readable_columns
        temp = cls.not_readable_columns
        temp = cls.writable_columns
        temp = cls.not_writable_columns
        super().populate_cache()


class RelationshipMixin(ModelMixinBase):
    """
    relationship mixin class.

    this class adds functionalities about relationship properties to its subclasses.
    """

    @class_property
    @fast_cache
    def relationships(cls):
        """
        gets all relationship property names of this entity.

        property names will be calculated once and cached.

        :rtype: tuple[str]
        """

        return cls.exposed_relationships + cls.not_exposed_relationships

    @class_property
    @fast_cache
    def exposed_relationships(cls):
        """
        gets exposed relationship property names of this entity.

        which are those that their name does not start with underscore `_`.
        property names will be calculated once and cached.

        :rtype: tuple[str]
        """

        info = sqla_inspect(cls)
        relationships = tuple(attr.key for attr in info.relationships
                              if cls.is_public(attr.key) is True)
        return relationships

    @class_property
    @fast_cache
    def not_exposed_relationships(cls):
        """
        gets not exposed relationship property names of this entity.

        which are those that their name starts with underscore `_`.
        property names will be calculated once and cached.

        :rtype: tuple[str]
        """

        info = sqla_inspect(cls)
        relationships = tuple(attr.key for attr in info.relationships
                              if cls.is_public(attr.key) is False)
        return relationships

    @classmethod
    def populate_cache(cls):
        """
        populates all related caches.
        """

        temp = cls.relationships
        super().populate_cache()


class HybridPropertyMixin(ModelMixinBase):
    """
    hybrid property mixin class.

    this class adds functionalities about all hybrid properties to its subclasses.
    """

    @class_property
    @fast_cache
    def all_getter_hybrid_properties(cls):
        """
        gets all getter hybrid property names of this entity.

        property names will be calculated once and cached.

        :rtype: tuple[str]
        """

        return cls.readable_hybrid_properties + cls.not_readable_hybrid_properties

    @class_property
    @fast_cache
    def all_setter_hybrid_properties(cls):
        """
        gets all setter hybrid property names of this entity.

        property names will be calculated once and cached.

        :rtype: tuple[str]
        """

        return cls.writable_hybrid_properties + cls.not_writable_hybrid_properties

    @class_property
    @fast_cache
    def readable_hybrid_properties(cls):
        """
        gets readable hybrid property names of this entity.

        readable hybrid properties are those that their name does
        not start with underscore `_`.
        property names will be calculated once and cached.

        :rtype: tuple[str]
        """

        info = sqla_inspect(cls)
        hybrid_properties = tuple(item.__name__ for item in info.all_orm_descriptors
                                  if isinstance(item, hybrid_property)
                                  and item.fget is not None
                                  and cls.is_public(item.__name__) is True)

        return hybrid_properties

    @class_property
    @fast_cache
    def not_readable_hybrid_properties(cls):
        """
        gets not readable hybrid property names of this entity.

        not readable hybrid properties are those that their
        name starts with underscore `_`.
        property names will be calculated once and cached.

        :rtype: tuple[str]
        """

        info = sqla_inspect(cls)
        hybrid_properties = tuple(item.__name__ for item in info.all_orm_descriptors
                                  if isinstance(item, hybrid_property)
                                  and item.fget is not None
                                  and cls.is_public(item.__name__) is False)

        return hybrid_properties

    @class_property
    @fast_cache
    def writable_hybrid_properties(cls):
        """
        gets writable hybrid property names of this entity.

        writable hybrid properties are those that their name does
        not start with underscore `_`.
        property names will be calculated once and cached.

        :rtype: tuple[str]
        """

        info = sqla_inspect(cls)
        hybrid_properties = tuple(item.__name__ for item in info.all_orm_descriptors
                                  if isinstance(item, hybrid_property)
                                  and item.fset is not None
                                  and cls.is_public(item.__name__) is True)

        return hybrid_properties

    @class_property
    @fast_cache
    def not_writable_hybrid_properties(cls):
        """
        gets not writable hybrid property names of this entity.

        not writable hybrid properties are those that their
        name starts with underscore `_`.
        property names will be calculated once and cached.

        :rtype: tuple[str]
        """

        info = sqla_inspect(cls)
        hybrid_properties = tuple(item.__name__ for item in info.all_orm_descriptors
                                  if isinstance(item, hybrid_property)
                                  and item.fset is not None
                                  and cls.is_public(item.__name__) is False)

        return hybrid_properties

    @classmethod
    def populate_cache(cls):
        """
        populates all related caches.
        """

        temp = cls.all_getter_hybrid_properties
        temp = cls.all_setter_hybrid_properties
        super().populate_cache()


class PrimaryKeyMixin(ModelMixinBase):
    """
    primary key mixin class.

    this class adds functionalities about primary keys to its subclasses.
    """

    def _is_primary_key_comparable(self, primary_key):
        """
        gets a value indicating that given primary key is comparable.

        the primary key is comparable if it is not None for single
        primary keys and if all the values in primary key tuple are
        not None for composite primary keys.

        :param object | tuple[object] primary_key: primary key value.

        :rtype: bool
        """

        if primary_key is None:
            return False

        if isinstance(primary_key, tuple):
            if len(primary_key) <= 0:
                return False
            else:
                return all(pk is not None for pk in primary_key)

        return True

    def primary_key(self, as_tuple=False):
        """
        gets the primary key value for this entity.

        it could be a single value or a tuple of values
        for composite primary keys.
        it could return None if no primary key is set for this entity.

        :param bool as_tuple: specifies that primary key value must be returned
                              as a tuple even if it's a single value.
                              defaults to False if not provided.

        :rtype: object | tuple[object]
        """

        columns = self.primary_key_columns
        if len(columns) <= 0:
            return None

        if as_tuple is False and len(columns) == 1:
            return getattr(self, columns[0])
        else:
            return tuple(getattr(self, col) for col in columns)

    @class_property
    @fast_cache
    def primary_key_columns(cls):
        """
        gets all primary key column names of this entity.

        column names will be calculated once and cached.

        note:
        as a column is either readable or not readable, so readable columns and
        not readable columns equal to all columns, as is for writable and
        not writable columns.

        :rtype: tuple[str]
        """

        return cls.readable_primary_key_columns + cls.not_readable_primary_key_columns

    @class_property
    @fast_cache
    def readable_primary_key_columns(cls):
        """
        gets the readable primary key column names of this entity.

        which are those that have `allow_read=True` in their definition
        and their name does not start with underscore `_`.
        column names will be calculated once and cached.

        :rtype: tuple[str]
        """

        info = sqla_inspect(cls)
        pk = tuple(info.get_property_by_column(col).key for col in info.primary_key
                   if cls.is_public(info.get_property_by_column(col).key) is True
                   and col.allow_read is True)

        return pk

    @class_property
    @fast_cache
    def not_readable_primary_key_columns(cls):
        """
        gets not readable primary key column names of this entity.

        which are those that have `allow_read=False` in their definition
        or their name starts with underscore `_`.
        column names will be calculated once and cached.

        :rtype: tuple[str]
        """

        info = sqla_inspect(cls)
        pk = tuple(info.get_property_by_column(col).key for col in info.primary_key
                   if cls.is_public(info.get_property_by_column(col).key) is False
                   or col.allow_read is False)

        return pk

    @class_property
    @fast_cache
    def writable_primary_key_columns(cls):
        """
        gets the writable primary key column names of this entity.

        which are those that have `allow_write=True` in their definition
        and their name does not start with underscore `_`.
        column names will be calculated once and cached.

        :rtype: tuple[str]
        """

        info = sqla_inspect(cls)
        pk = tuple(info.get_property_by_column(col).key for col in info.primary_key
                   if cls.is_public(info.get_property_by_column(col).key) is True
                   and col.allow_write is True)

        return pk

    @class_property
    @fast_cache
    def not_writable_primary_key_columns(cls):
        """
        gets not writable primary key column names of this entity.

        which are those that have `allow_write=False` in their definition
        or their name starts with underscore `_`.
        column names will be calculated once and cached.

        :rtype: tuple[str]
        """

        info = sqla_inspect(cls)
        pk = tuple(info.get_property_by_column(col).key for col in info.primary_key
                   if cls.is_public(info.get_property_by_column(col).key) is False
                   or col.allow_write is False)

        return pk

    @classmethod
    def populate_cache(cls):
        """
        populates all related caches.
        """

        temp = cls.readable_primary_key_columns
        temp = cls.not_readable_primary_key_columns
        temp = cls.writable_primary_key_columns
        temp = cls.not_writable_primary_key_columns
        super().populate_cache()


class ForeignKeyMixin(ModelMixinBase):
    """
    foreign key mixin class.

    this class adds functionalities about foreign keys to its subclasses.
    """

    @class_property
    @fast_cache
    def foreign_key_columns(cls):
        """
        gets all foreign key column names of this entity.

        column names will be calculated once and cached.
        note that those foreign keys which are also a primary key, will not
        be included in this list.

        note:
        as a column is either readable or not readable, so readable columns and
        not readable columns equal to all columns, as is for writable and
        not writable columns.

        :rtype: tuple[str]
        """

        return cls.readable_foreign_key_columns + cls.not_readable_foreign_key_columns

    @class_property
    @fast_cache
    def readable_foreign_key_columns(cls):
        """
        gets the readable foreign key column names of this entity.

        which are those that have `allow_read=True` in their definition
        and their name does not start with underscore `_`.
        column names will be calculated once and cached.
        note that those foreign keys which are also a primary key, will not
        be included in this list.

        :rtype: tuple[str]
        """

        info = sqla_inspect(cls)
        fk = tuple(attr.key for attr in info.column_attrs
                   if attr.columns[0].is_foreign_key is True
                   and attr.columns[0].primary_key is False
                   and cls.is_public(attr.key) is True
                   and attr.columns[0].allow_read is True)

        return fk

    @class_property
    @fast_cache
    def not_readable_foreign_key_columns(cls):
        """
        gets not readable foreign key column names of this entity.

        which are those that have `allow_read=False` in their definition
        or their name starts with underscore `_`.
        column names will be calculated once and cached.
        note that those foreign keys which are also a primary key, will not
        be included in this list.

        :rtype: tuple[str]
        """

        info = sqla_inspect(cls)
        fk = tuple(attr.key for attr in info.column_attrs
                   if attr.columns[0].is_foreign_key is True
                   and attr.columns[0].primary_key is False and
                   (cls.is_public(attr.key) is False or
                    attr.columns[0].allow_read is False))

        return fk

    @class_property
    @fast_cache
    def writable_foreign_key_columns(cls):
        """
        gets the writable foreign key column names of this entity.

        which are those that have `allow_write=True` in their definition
        and their name does not start with underscore `_`.
        column names will be calculated once and cached.
        note that those foreign keys which are also a primary key, will not
        be included in this list.

        :rtype: tuple[str]
        """

        info = sqla_inspect(cls)
        fk = tuple(attr.key for attr in info.column_attrs
                   if attr.columns[0].is_foreign_key is True
                   and attr.columns[0].primary_key is False
                   and cls.is_public(attr.key) is True
                   and attr.columns[0].allow_write is True)

        return fk

    @class_property
    @fast_cache
    def not_writable_foreign_key_columns(cls):
        """
        gets not writable foreign key column names of this entity.

        which are those that have `allow_write=False` in their definition
        or their name starts with underscore `_`.
        column names will be calculated once and cached.
        note that those foreign keys which are also a primary key, will not
        be included in this list.

        :rtype: tuple[str]
        """

        info = sqla_inspect(cls)
        fk = tuple(attr.key for attr in info.column_attrs
                   if attr.columns[0].is_foreign_key is True
                   and attr.columns[0].primary_key is False and
                   (cls.is_public(attr.key) is False or
                    attr.columns[0].allow_write is False))

        return fk

    @classmethod
    def populate_cache(cls):
        """
        populates all related caches.
        """

        temp = cls.readable_foreign_key_columns
        temp = cls.not_readable_foreign_key_columns
        temp = cls.writable_foreign_key_columns
        temp = cls.not_writable_foreign_key_columns
        super().populate_cache()


class AttributeMixin(ModelMixinBase):
    """
    attribute mixin class.

    this class adds functionalities about all attributes to its subclasses.
    attributes includes pk, fk, columns, relationships and hybrid properties.
    """

    @class_property
    @fast_cache
    def all_column_attributes(cls):
        """
        gets an immutable dict of all column attributes of this entity.

        the result will be calculated once and cached per entity type.

        :returns: CoreImmutableDict(str name, CoreColumn column)
        :rtype: CoreImmutableDict
        """

        result = dict()
        info = sqla_inspect(cls)
        for attr in info.column_attrs:
            result[attr.key] = attr.columns[0]

        return CoreImmutableDict(result)

    @class_property
    @fast_cache
    def all_reverse_column_attributes(cls):
        """
        gets an immutable dict of all reverse column attributes of this entity.

        this is the opposite of `all_column_attributes` value. the result
        dict keys are column instances and their values are attribute names.
        the result will be calculated once and cached per entity type.

        :returns: CoreImmutableDict(CoreColumn column, str name)
        :rtype: CoreImmutableDict
        """

        result = dict()
        for name, column in cls.all_column_attributes.items():
            result[column] = name

        return CoreImmutableDict(result)

    @class_property
    @fast_cache
    def all_instrumented_attributes(cls):
        """
        gets a tuple of all instrumented attributes of this entity.

        instrumented attributes are the attributes that are returned
        by sqlalchemy when you get a column of a model at class level.

        for example:

        CarEntity.name -> InstrumentedAttribute
        HumanEntity.age -> InstrumentedAttribute

        the result will be calculated once and cached per entity type.

        :rtype: tuple
        """

        all_columns = cls.primary_key_columns + cls.foreign_key_columns + cls.all_columns
        result = []
        for name in all_columns:
            attribute = getattr(cls, name)
            result.append(attribute)

        return tuple(result)

    @class_property
    @fast_cache
    def all_attributes(cls):
        """
        gets all attribute names of current entity.

        attribute names will be calculated once and cached.

        :rtype: tuple[str]
        """

        return cls.all_readable_attributes + cls.all_not_readable_attributes

    @class_property
    @fast_cache
    def all_readable_attributes(cls):
        """
        gets all readable attribute names of current entity.

        which are those that have `allow_read=True` (only for columns) in
        their definition and their name does not start with underscore `_`.
        attribute names will be calculated once and cached.

        :rtype: tuple[str]
        """

        return cls.readable_primary_key_columns + cls.readable_foreign_key_columns + \
            cls.readable_columns + cls.exposed_relationships + cls.readable_hybrid_properties

    @class_property
    @fast_cache
    def all_not_readable_attributes(cls):
        """
        gets all not readable attribute names of current entity.

        which are those that have `allow_read=False` (only for columns) in
        their definition or their name starts with underscore `_`.
        attribute names will be calculated once and cached.

        :rtype: tuple[str]
        """

        return cls.not_readable_primary_key_columns + cls.not_readable_foreign_key_columns + \
            cls.not_readable_columns + cls.not_exposed_relationships + \
            cls.not_readable_hybrid_properties

    @class_property
    @fast_cache
    def all_writable_attributes(cls):
        """
        gets all writable attribute names of current entity.

        which are those that have `allow_write=True` (only for columns) in
        their definition and their name does not start with underscore `_`.
        attribute names will be calculated once and cached.

        :rtype: tuple[str]
        """

        return cls.writable_primary_key_columns + cls.writable_foreign_key_columns + \
            cls.writable_columns + cls.exposed_relationships + cls.writable_hybrid_properties

    @class_property
    @fast_cache
    def all_not_writable_attributes(cls):
        """
        gets all not writable attribute names of current entity.

        which are those that have `allow_write=False` (only for columns) in
        their definition or their name starts with underscore `_`.
        attribute names will be calculated once and cached.

        :rtype: tuple[str]
        """

        return cls.not_writable_primary_key_columns + cls.not_writable_foreign_key_columns + \
            cls.not_writable_columns + cls.not_exposed_relationships + \
            cls.not_writable_hybrid_properties

    @classmethod
    def is_public(cls, name):
        """
        gets a value indicating that an attribute with given name is public.

        it simply checks that the given name starts with an underscore `_`.
        if so, it is considered as not public.

        :param str name: attribute name.

        :rtype: bool
        """

        return not name.startswith('_')

    @classmethod
    def populate_cache(cls):
        """
        populates all related caches.
        """

        temp = cls.all_column_attributes
        temp = cls.all_reverse_column_attributes
        temp = cls.all_instrumented_attributes
        temp = cls.all_readable_attributes
        temp = cls.all_not_readable_attributes
        temp = cls.all_writable_attributes
        temp = cls.all_not_writable_attributes
        super().populate_cache()


class ConverterMixin:
    """
    converter mixin class.

    this class adds functionalities to convert dict to
    entity and vice versa to its subclasses.
    """

    # maximum allowed depth for conversion.
    # note that higher depth values may cause performance issues or
    # application failure in some cases. so if you do not know how
    # much depth is required for conversion, start without providing depth.
    # this value could be overridden in concrete entities if required.
    MAX_DEPTH = 5

    def to_dict(self, **options):
        """
        converts the entity into a dict and returns it.

        it could convert primary keys, foreign keys, other columns, hybrid
        properties and also relationship properties if `depth` is provided.
        the result dict by default only contains the readable attributes of the
        entity which are those that have `allow_read=True` (only for columns) and
        their name does not start with underscore `_`.

        :keyword SECURE_TRUE | SECURE_FALSE readable: specifies that any column or attribute
                                                      which has `allow_read=False` or its name
                                                      starts with underscore `_`, should not
                                                      be included in result dict. defaults to
                                                      `SECURE_TRUE` if not provided.

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
                                                           available in result, they will
                                                           be ignored.

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

        :raises InvalidDepthProvidedError: invalid depth provided error.

        :rtype: dict
        """

        all_attributes = None
        relations = None
        requested_columns, rename, excluded_columns = self._extract_conditions(**options)
        readable = options.get('readable', SECURE_TRUE)

        depth = options.get('depth', None)
        if depth is None:
            depth = config_services.get('database', 'conversion', 'default_depth')

        if readable is SECURE_FALSE:
            all_attributes = self.all_attributes
            relations = self.relationships
        else:
            all_attributes = self.all_readable_attributes
            relations = self.exposed_relationships

        requested_relationships = []
        all_attributes = set(all_attributes)
        if len(requested_columns) > 0:
            requested_columns = requested_columns.intersection(all_attributes)
        else:
            requested_columns = all_attributes.difference(excluded_columns)

        result = DTO()
        for col in requested_columns:
            if col in relations:
                requested_relationships.append(col)
            else:
                result[rename.get(col, col)] = getattr(self, col)

        if depth > 0 and len(requested_relationships) > 0:
            if depth > self.MAX_DEPTH:
                raise InvalidDepthProvidedError('Maximum valid "depth" for conversion '
                                                'is [{max_depth}]. provided depth '
                                                '[{invalid_depth}] is invalid.'
                                                .format(max_depth=self.MAX_DEPTH,
                                                        invalid_depth=depth))

            options.update(depth=depth - 1)
            for relation in requested_relationships:
                value = getattr(self, relation)
                new_name = rename.get(relation, relation)
                result[new_name] = None
                if value is not None:
                    if isinstance(value, LIST_TYPES):
                        result[new_name] = []
                        if len(value) > 0:
                            for entity in value:
                                result[new_name].append(entity.to_dict(**options))
                    else:
                        result[new_name] = value.to_dict(**options)

        return result

    def from_dict(self, **kwargs):
        """
        updates the column values of this entity with values in keyword arguments.

        it could fill primary keys, foreign keys, other columns, hybrid properties
        and also relationship properties provided in keyword arguments.
        note that relationship values must be entities. this method could
        not convert relationships which are dict, into entities.

        :keyword SECURE_TRUE | SECURE_FALSE writable: specifies that any column which has
                                                      `allow_write=False` or its name starts
                                                      with underscore `_`, should not be
                                                      populated from given values. this
                                                      is useful if you want to fill an
                                                      entity with keyword arguments passed
                                                      from client and then doing the
                                                      validation. but do not want to expose
                                                      a security risk. especially in update
                                                      operations. defaults to `SECURE_TRUE`
                                                      if not provided.

        :keyword SECURE_TRUE | SECURE_FALSE ignore_invalid_column: specifies that if a key is
                                                                   not available in entity
                                                                   columns, do not raise an
                                                                   error. defaults to
                                                                   `SECURE_TRUE` if not provided.

        :keyword SECURE_TRUE | SECURE_FALSE ignore_pk: specifies that any primary key column
                                                       should not be populated with given
                                                       values. this is useful if you want to
                                                       fill an entity with keyword arguments
                                                       passed from client and then doing the
                                                       validation. but do not want to let user
                                                       set primary keys and exposes a security
                                                       risk. especially in update operations.
                                                       defaults to `SECURE_TRUE` if not provided.

        :keyword SECURE_TRUE | SECURE_FALSE ignore_fk: specifies that any foreign key column
                                                       should not be populated with given
                                                       values. this is useful if you want
                                                       to fill an entity with keyword arguments
                                                       passed from client and then doing the
                                                       validation. but do not want to let user
                                                       set foreign keys and exposes a security
                                                       risk. especially in update operations.
                                                       defaults to `SECURE_FALSE` if not provided.

        :keyword SECURE_TRUE | SECURE_FALSE ignore_relationships: specifies that any relationship
                                                                  property should not be populated
                                                                  with given values. defaults to
                                                                  `SECURE_TRUE` if not provided.

        :keyword SECURE_TRUE | SECURE_FALSE populate_all: specifies that all available values
                                                          must be populated from provided keyword
                                                          arguments. if set to `SECURE_TRUE`, all
                                                          other parameters will be bypassed.
                                                          this is for convenience of usage.
                                                          defaults to `SECURE_FALSE` if not
                                                          provided.

        :raises ColumnNotExistedError: column not existed error.
        """

        ignore_invalid = kwargs.pop('ignore_invalid_column', SECURE_TRUE)
        populate_all = kwargs.pop('populate_all', SECURE_FALSE)
        if populate_all is SECURE_TRUE:
            writable = SECURE_FALSE
            ignore_pk = SECURE_FALSE
            ignore_fk = SECURE_FALSE
            ignore_relationships = SECURE_FALSE
        else:
            writable = kwargs.pop('writable', SECURE_TRUE)
            ignore_pk = kwargs.pop('ignore_pk', SECURE_TRUE)
            ignore_fk = kwargs.pop('ignore_fk', SECURE_FALSE)
            ignore_relationships = kwargs.pop('ignore_relationships', SECURE_TRUE)

        accessible_columns = self.writable_columns
        if writable is SECURE_FALSE:
            accessible_columns = self.all_columns

        accessible_hybrid_properties = self.writable_hybrid_properties
        if writable is SECURE_FALSE:
            accessible_hybrid_properties = self.all_setter_hybrid_properties

        accessible_pk = ()
        if ignore_pk is SECURE_FALSE:
            if writable is SECURE_FALSE:
                accessible_pk = self.primary_key_columns
            else:
                accessible_pk = self.writable_primary_key_columns

        accessible_fk = ()
        if ignore_fk is not SECURE_TRUE:
            if writable is SECURE_FALSE:
                accessible_fk = self.foreign_key_columns
            else:
                accessible_fk = self.writable_foreign_key_columns

        accessible_relationships = ()
        if ignore_relationships is SECURE_FALSE:
            if writable is SECURE_FALSE:
                accessible_relationships = self.relationships
            else:
                accessible_relationships = self.exposed_relationships

        all_accessible_columns = accessible_pk + accessible_fk + \
            accessible_columns + accessible_relationships + accessible_hybrid_properties

        provided_columns = set(kwargs.keys())
        result_columns = set(all_accessible_columns).intersection(provided_columns)
        if ignore_invalid is SECURE_FALSE:
            not_existed = provided_columns.difference(result_columns)
            if len(not_existed) > 0:
                raise ColumnNotExistedError('Provided columns, relationships or properties '
                                            '{columns} are not available in entity [{entity}].'
                                            .format(columns=list(not_existed),
                                                    entity=self.get_fully_qualified_name()))

        for column in result_columns:
            setattr(self, column, kwargs.get(column))

    def set_attribute(self, name, value, silent=True):
        """
        sets the provided value for attribute with given name.

        it only could set value for writable attributes, which are those that
        have `allow_write=True` in their definition (only for columns) and
        their name does not start with underscore `_`.

        this method is implemented to be used in validator package.
        it is not recommended to be used in application code.
        use `from_dict` method instead.

        :param str name: attribute name.
        :param object value: value to be set for attribute.

        :param bool silent: specifies that if there is no attribute
                            with given name, ignore it instead of error.
                            defaults to True.

        :raises ColumnNotExistedError: column not existed error.
        """

        if name in self.all_writable_attributes:
            setattr(self, name, value)
            return

        if silent is False:
            raise ColumnNotExistedError('Provided column, relationship or property '
                                        '[{column}] is not available in entity [{entity}].'
                                        .format(column=name,
                                                entity=self.get_fully_qualified_name()))

    def _extract_conditions(self, **options):
        """
        extracts all conditions available in given options.

        it extracts columns, rename and exclude values.

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
                                                           available in result, they will
                                                           be ignored.

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
                                                                    if there is `CarEntity` and
                                                                    `PersonEntity`, it should be
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

        :returns: tuple[set[str column_name],
                        dict[str original_column, str new_column],
                        set[str excluded_column]]

        :rtype: tuple[set[str], dict[str, str], set[str]]
        """

        columns = options.get('columns', None)
        rename = options.get('rename', None)
        exclude = options.get('exclude', None)

        if isinstance(columns, dict):
            columns = columns.get(self.get_class_name(), None)

        if isinstance(rename, dict) and len(rename) > 0 and \
                isinstance(list(rename.values())[0], dict):

            rename = rename.get(self.get_class_name(), None)

        if isinstance(exclude, dict):
            exclude = exclude.get(self.get_class_name(), None)

        if columns is None:
            columns = []

        if rename is None:
            rename = {}

        if exclude is None:
            exclude = []

        columns = set(columns)
        exclude = set(exclude)
        return columns.difference(exclude), rename, exclude


class MagicMethodMixin(ModelMixinBase):
    """
    magic method mixin class.

    this class adds different magic method implementations to its subclasses.
    """

    def __eq__(self, other):
        """
        gets the equality comparison result.

        first, it compares primary keys if they have value in both entities
        and both entities have a common root parent.
        otherwise it compares them using python default memory location comparison.

        :param CoreEntity other: other entity to compare for equality.

        :rtype: bool
        """

        if isinstance(other, self.root_base_class):
            if self._is_primary_key_comparable(self.primary_key()) is True:
                return self.primary_key() == other.primary_key()
            else:
                return self is other

        return False

    def __ne__(self, other):
        """
        gets the not equality comparison result.

        :param CoreEntity other: other entity to compare for not equality.

        :rtype: bool
        """

        return not self == other

    def __hash__(self):
        """
        gets the hash of current entity.

        if the entity has valid primary key values, it will be considered
        in hash generation. otherwise it falls back to general hash generation
        based on python defaults.

        :rtype: int
        """

        if self._is_primary_key_comparable(self.primary_key()) is True:
            return hash('{root_base}.{pk}'.format(root_base=self.root_base_class,
                                                  pk=self.primary_key()))

        return super().__hash__()

    def __str__(self):
        """
        gets the string representation of current entity.

        :rtype: str
        """

        return '{fullname} -> {pk}'.format(fullname=self.get_fully_qualified_name(),
                                           pk=self.primary_key())

    @class_property
    @fast_cache
    def root_base_class(cls):
        """
        gets root base class of this entity.

        root base class is the class which is direct subclass
        of declarative base class (which by default is CoreEntity)
        in inheritance hierarchy.

        for example if you use pyrin's default CoreEntity as your base model:
        {CoreEntity -> BaseEntity, A -> CoreEntity, B -> A, C -> B}
        then, root base class of A, B and C is A.

        if you implement a new base class named MyNewDeclarativeBase as base model:
        {MyNewDeclarativeBase -> BaseEntity, A -> MyNewDeclarativeBase, B -> A, C -> B}
        then, root base class of A, B and C is A.

        the inheritance rule also supports multi-branch hierarchy. for example:
        {CoreEntity -> BaseEntity, A -> CoreEntity, B -> A, C -> A}
        then, root base class of A, B and C is A.

        root base class will be calculated once and cached per entity type.

        :rtype: type
        """

        bases = inspect.getmro(cls)
        root_base_entity_index = bases.index(cls.declarative_base_class) - 1
        base = bases[root_base_entity_index]
        return base

    @class_property
    def declarative_base_class(cls):
        """
        gets declarative base class of application.

        :rtype: type
        """

        base = cls._get_declarative_base_class()
        if base is None:
            bases = inspect.getmro(cls)
            base_entity_index = bases.index(cls._base_entity_class)
            potential_declarative_bases = bases[0:base_entity_index]
            base = cls._extract_declarative_base(potential_declarative_bases)
            cls._set_declarative_base_class(base)

        return base

    @classmethod
    def _extract_declarative_base(cls, types):
        """
        extracts the first declarative base found from given types.

        returns None if not found.

        :param tuple[type] types: class types to extract declarative base from them.

        :rtype: type
        """

        for item in types:
            try:
                sqla_inspect(item)
            except NoInspectionAvailable:
                return item

        return None

    @classmethod
    def _set_declarative_base_class(cls, declarative_base_class):
        """
        sets declarative base class of application.

        the value will be set and shared for all entities because there
        should be only one declarative base class.

        :param type declarative_base_class: a class type of application declarative base class.
                                            by default, it would be `CoreEntity` class.
        """

        cls._validate_declarative_base_class(declarative_base_class)
        MagicMethodMixin._declarative_base_class = declarative_base_class

    @classmethod
    def _get_declarative_base_class(cls):
        """
        gets declarative base class of application.

        returns None if it's not set.

        :rtype: type
        """

        return getattr(MagicMethodMixin, '_declarative_base_class', None)

    @class_property
    @abstractmethod
    def _base_entity_class(cls):
        """
        gets base entity class of application.

        this method must be overridden in `BaseEntity` class.
        it should return type of `BaseEntity` class itself.
        this method is required to overcome circular dependency problem as mixin
        module could not import `BaseEntity` because `BaseEntity` itself references
        to mixin module. and also we could not inject `BaseEntity` dependency through
        `__init__()` method of `MagicMethodMixin` class, because sqlalchemy does not
        call `__init__()` method of entities for populating database results, so
        `__init__()` call is not guaranteed and will only take place on user code.
        so we have to define this method to get `BaseEntity` type here.
        and this is more beautiful then importing `BaseEntity` inside a method
        of `MagicMethodMixin` class.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: type
        """

        raise CoreNotImplementedError()

    @classmethod
    def _validate_declarative_base_class(cls, declarative_base_class):
        """
        validates the given declarative base class.

        :param type declarative_base_class: a class type of application declarative base class.
                                            by default, it would be `CoreEntity` class.

        :raises InvalidDeclarativeBaseTypeError: invalid declarative base type error.
        """

        if declarative_base_class is None or not inspect.isclass(declarative_base_class):
            raise InvalidDeclarativeBaseTypeError('Input parameter [{declarative}] '
                                                  'is not a class.'
                                                  .format(declarative=declarative_base_class))

        if not issubclass(declarative_base_class, cls._base_entity_class):
            raise InvalidDeclarativeBaseTypeError('Input parameter [{declarative}] '
                                                  'in not a subclass of [{base}].'
                                                  .format(declarative=declarative_base_class,
                                                          base=cls._base_entity_class))

        if declarative_base_class is not model_services.get_declarative_base():
            print_warning('You have implemented a new declarative base type [{new}] '
                          'in your application. to make everything works as expected '
                          'you must override "pyrin.database.model.ModelManager.'
                          'get_declarative_base()" method in your application inside '
                          '"database.model" package. for more information on how to do '
                          'that or how to ignore it, see the documentation of specified '
                          'method.'.format(new=declarative_base_class))

    @classmethod
    def populate_cache(cls):
        """
        populates all related caches.
        """

        temp = cls.root_base_class
        super().populate_cache()


class QueryMixin:
    """
    query mixin class.

    this class adds query method to its subclasses.
    the query method will always use the correct session
    based on request context availability.
    """

    @classmethod
    def query(cls, *entities, **options):
        """
        gets the query object to perform queries on it.

        it always uses the correct session based on request context availability.

        :param BaseEntity entities: entities or columns to use them in query.
                                    if not provided, it uses all columns of this entity.

        :keyword type | tuple[type] scope: class type of the entities that this
                                           query instance will work on. if the
                                           query is working on multiple entities,
                                           this value must be a tuple of all class
                                           types of that entities.

                                           for example: if you set
                                           `entities=SomeEntity.id, AnotherEntity.name`
                                           you should leave `scope=None` to skip validation
                                           or you could set
                                           `scope=(SomeEntity, AnotherEntity)`
                                           this way validation succeeds, but if
                                           you set `scope=SomeEntity`
                                           then the query will not be executed
                                           and an error will be raised.

        :raises ColumnsOutOfScopeError: columns out of scope error.

        :rtype: CoreQuery
        """

        store = get_current_store()
        used_entities = entities
        if entities is None or len(entities) <= 0:
            used_entities = (cls,)

        return store.query(*used_entities, **options)


class CRUDMixin:
    """
    crud mixin class.

    this class adds CRUD functionalities to is subclasses.
    it includes save, update and delete.
    it uses the correct session based on request context availability.
    """

    def save(self, flush=False):
        """
        saves the current entity.

        :param bool flush: flush changes to database at the end.
                           defaults to False if not provided.
                           this would be helpful if you need to get
                           the autogenerated values by database such as sequences.

        :rtype: BaseEntity
        """

        store = get_current_store()
        store.add(self)

        if flush is True:
            store.flush()

        return self

    def update(self, flush=False, **kwargs):
        """
        updates the column values of this entity with values in keyword arguments.

        then persists changes into database.
        it could fill primary keys, foreign keys, other columns, hybrid properties
        and also relationship properties provided in keyword arguments.
        note that relationship values must be entities. this method could
        not convert relationships which are dict, into entities.

        :param bool flush: flush changes to database at the end.
                           defaults to False if not provided.
                           this would be helpful if you need to get
                           the autogenerated values by database such as sequences.

        :keyword SECURE_TRUE | SECURE_FALSE writable: specifies that any column which has
                                                      `allow_write=False` or its name starts
                                                      with underscore `_`, should not be
                                                      populated from given values. this
                                                      is useful if you want to fill an
                                                      entity with keyword arguments passed
                                                      from client and then doing the
                                                      validation. but do not want to expose
                                                      a security risk. especially in update
                                                      operations. defaults to `SECURE_TRUE`
                                                      if not provided.

        :keyword SECURE_TRUE | SECURE_FALSE ignore_invalid_column: specifies that if a key is
                                                                   not available in entity
                                                                   columns, do not raise an
                                                                   error. defaults to
                                                                   `SECURE_TRUE` if not provided.

        :keyword SECURE_TRUE | SECURE_FALSE ignore_pk: specifies that any primary key column
                                                       should not be populated with given
                                                       values. this is useful if you want to
                                                       fill an entity with keyword arguments
                                                       passed from client and then doing the
                                                       validation. but do not want to let user
                                                       set primary keys and exposes a security
                                                       risk. especially in update operations.
                                                       defaults to `SECURE_TRUE` if not provided.

        :keyword SECURE_TRUE | SECURE_FALSE ignore_fk: specifies that any foreign key column
                                                       should not be populated with given
                                                       values. this is useful if you want
                                                       to fill an entity with keyword arguments
                                                       passed from client and then doing the
                                                       validation. but do not want to let user
                                                       set foreign keys and exposes a security
                                                       risk. especially in update operations.
                                                       defaults to `SECURE_FALSE` if not provided.

        :keyword SECURE_TRUE | SECURE_FALSE ignore_relationships: specifies that any relationship
                                                                  property should not be populated
                                                                  with given values. defaults to
                                                                  `SECURE_TRUE` if not provided.

        :keyword SECURE_TRUE | SECURE_FALSE populate_all: specifies that all available values
                                                          must be populated from provided keyword
                                                          arguments. if set to `SECURE_TRUE`, all
                                                          other parameters will be bypassed.
                                                          this is for convenience of usage.
                                                          defaults to `SECURE_FALSE` if not
                                                          provided.

        :keyword SECURE_TRUE | SECURE_FALSE prefetch_complex_defaults: specifies that all columns
                                                                       that have default values
                                                                       for update must fetch their
                                                                       default value if no value
                                                                       is provided for them in
                                                                       `kwargs`.
                                                                       note that scalar default
                                                                       values will always be
                                                                       fetched and this option is
                                                                       only for sequence or
                                                                       callable default values.
                                                                       defaults to `SECURE_TRUE`
                                                                       if not provided.

        :note prefetch_complex_defaults: for callable defaults we have to pass
                                         `ExecutionContext` as None because there is no
                                         such context in prefetch time. so if your callable
                                         default actually needs a valid context, you can not
                                         prefetch its value and must disable prefetching by
                                         passing `prefetch_complex_defaults=SECURE_FALSE`.
                                         otherwise unexpected behavior may occur.

        :raises ColumnNotExistedError: column not existed error.

        :rtype: BaseEntity
        """

        self.from_dict(**kwargs)
        self.prefetch_update_defaults(**kwargs)
        return self.save(flush=flush)

    def delete(self, flush=False):
        """
        deletes the current entity.

        :param bool flush: flush changes to database at the end.
                           defaults to False if not provided.
                           this would be helpful if you need to get
                           the autogenerated values by database such as sequences.
        """

        store = get_current_store()
        store.delete(self)

        if flush is True:
            store.flush()


class MetadataMixin:
    """
    metadata mixin class.

    this class provides a simple and extensible api for declarative models configuration.
    """

    # table name
    _table = None

    # table args
    _schema = None
    _extend_existing = None

    # specifies that this entity is abstract.
    # abstract entities does not represent any table on database.
    _abstract = False

    # a list of entity column instances or table column names to
    # create unique constraint for them.
    # for example:
    # _unique_on = name -> single column.
    # _unique_on = name, age -> multiple columns in one constraint.
    # _unique_on = identity, (name, age), username -> multiple columns in three constraints.
    _unique_on = None

    # mapper args
    _polymorphic_on = None
    _polymorphic_identity = None
    _concrete = None

    @classmethod
    @fast_cache
    def _get_unique_constraints(cls):
        """
        gets required unique constraints for this entity.

        :rtype: tuple[UniqueConstraint]
        """

        if cls._unique_on is None:
            return tuple()

        uniques = misc_utils.make_iterable(cls._unique_on, tuple)
        is_multiple = False
        for item in uniques:
            if isinstance(item, LIST_TYPES):
                is_multiple = True
                break

        constraints = []
        if is_multiple is False:
            constraints.append(UniqueConstraint(*uniques))
        else:
            for item in uniques:
                iterable_item = misc_utils.make_iterable(item, tuple)
                constraints.append(UniqueConstraint(*iterable_item))

        return tuple(constraints)

    @declared_attr
    def __abstract__(cls):
        """
        gets a value indicating that this entity is abstract.

        abstract entities does not represent any table on database.

        :rtype: bool
        """

        return cls._abstract

    @declared_attr
    def __tablename__(cls):
        """
        gets the table name of current entity type.

        it returns the value of `_table` class attribute of entity.

        :rtype: str
        """

        return cls._table

    @declared_attr
    @fast_cache
    def __table_args__(cls):
        """
        gets the table args of current entity type.

        it returns a dict or tuple of all configured table args.

        for example: {'schema': 'database_name.schema_name',
                      'extend_existing': True}

        :rtype: dict | tuple
        """

        table_args = dict()
        if cls._schema is not None:
            table_args.update(schema=cls._schema)

        if cls._extend_existing is not None:
            table_args.update(extend_existing=cls._extend_existing)

        unique_constraints = cls._get_unique_constraints()
        extra_args = cls._customize_table_args(table_args)
        if extra_args is not None:
            extra_args = misc_utils.make_iterable(extra_args, tuple)
        else:
            extra_args = tuple()

        all_args = unique_constraints + extra_args
        if len(all_args) <= 0:
            return table_args

        return all_args + (table_args,)

    @declared_attr
    @fast_cache
    def __mapper_args__(cls):
        """
        gets the mapper args of current entity type.

        :rtype: dict
        """

        mapper_args = dict()
        if cls._polymorphic_on is not None:
            mapper_args.update(polymorphic_on=cls._polymorphic_on)

        if cls._polymorphic_identity is not None:
            mapper_args.update(polymorphic_identity=cls._polymorphic_identity)

        if cls._concrete is not None:
            mapper_args.update(concrete=cls._concrete)

        cls._customize_mapper_args(mapper_args)
        return mapper_args

    @classmethod
    def _customize_table_args(cls, table_args):
        """
        customizes different table args for current entity type.

        this method is intended to be overridden by subclasses to customize
        table args per entity type if the required customization needs extra work.
        it must modify input dict values in-place if required.
        if other table args must be added (ex. UniqueConstraint or CheckConstraint ...)
        it must return those as a tuple. it could also return a single object as
        extra table arg (ex. a single UniqueConstraint).
        if no changes are required this method must return None.

        :param dict table_args: a dict containing different table args.
                                any changes to this dict must be done in-place.

        :rtype: tuple | object
        """

        return None

    @classmethod
    def _customize_mapper_args(cls, mapper_args):
        """
        customizes different mapper args for current entity type.

        this method is intended to be overridden by subclasses to customize
        mapper args per entity type if the required customization needs extra work.
        it must modify values of input dict in-place if required.

        :param dict mapper_args: a dict containing different mapper args.
        """
        pass

    @class_property
    def table_name(cls):
        """
        gets the table name that this entity represents in database.

        :rtype: str
        """

        return cls._table

    @class_property
    def table_schema(cls):
        """
        gets the table schema that this entity represents in database.

        it might be `None` if schema has not been set for this entity.

        :rtype: str
        """

        return cls._schema

    @class_property
    def table_fullname(cls):
        """
        gets the table fullname that this entity represents in database.

        fullname is `schema.table_name` if schema is available, otherwise it
        defaults to `table_name`.

        :rtype: str
        """

        if cls.table_schema is not None:
            return '{schema}.{name}'.format(schema=cls.table_schema, name=cls.table_name)
        else:
            return cls.table_name

    @class_property
    def extend_existing(cls):
        """
        gets a value indicating that this entity extends another entity.

        :rtype: bool
        """

        return cls._extend_existing


class ModelCacheMixin(TypedCacheMixin):
    """
    model cache mixin class.

    this class adds caching support to its subclasses.
    """

    _container = {}


class DefaultPrefetchMixin(ModelMixinBase):
    """
    default prefetch mixin class.

    this class adds support to prefetch columns with default or onupdate
    values without flush or commit.
    """

    @classmethod
    def _get_column_attribute(cls, name):
        """
        gets column attribute with given name.

        :param str name: column name.

        :rtype: CoreColumn
        """

        return cls.all_column_attributes.get(name)

    def _get_insert_default_value(self, column):
        """
        gets the insert default value for given column.

        :param str column: column name.

        :returns: object
        """

        attribute = self._get_column_attribute(column)
        return self._fetch_default_value(attribute.default)

    def _get_update_default_value(self, column):
        """
        gets the update default value for given column.

        :param str column: column name.

        :returns: object
        """

        attribute = self._get_column_attribute(column)
        return self._fetch_default_value(attribute.onupdate)

    def _set_insert_default(self, column):
        """
        sets the insert default value to the given column.

        :param str column: column name.
        """

        value = self._get_insert_default_value(column)
        setattr(self, column, value)

    def _set_update_default(self, column):
        """
        sets the update default value to the given column.

        :param str column: column name.
        """

        value = self._get_update_default_value(column)
        setattr(self, column, value)

    @classmethod
    def _fetch_default_value(cls, default):
        """
        fetches the value from given default clause.

        note that for callable defaults we have to pass `ExecutionContext` as None
        because there is no such context in prefetch time. so if your callable default
        actually needs a valid context, you can not prefetch its value and must disable
        prefetching by passing `prefetch_complex_defaults=False` in corresponding method.
        otherwise unexpected behavior may occur.

        :param ColumnDefault default: column default instance.

        :returns: object
        """

        # the order of if conditions must be exactly this way. because
        # 'Sequence' object does not have the other attributes.
        if default.is_sequence:
            store = get_current_store()
            return store.execute(default.next_value()).scalar()
        elif default.is_scalar:
            return default.arg
        elif default.is_callable:
            return default.arg(None)

        return cls._fetch_default_value_extended(default)

    @classmethod
    @abstractmethod
    def _fetch_default_value_extended(cls, default):
        """
        fetches the value from given default clause.

        this method is intended to be overridden in subclasses to modify or extend
        prefetching default values. for example to support `ClauseElement` defaults.

        :param ColumnDefault default: column default instance.

        :raises CoreNotImplementedError: core not implemented error.

        :returns: object
        """

        raise CoreNotImplementedError()

    @class_property
    @fast_cache
    def columns_with_scalar_insert_default(cls):
        """
        gets column names that have scalar default values for insert.

        :rtype: tuple[str]
        """

        all_columns = cls.primary_key_columns + cls.all_columns + cls.foreign_key_columns
        result = []
        for name in all_columns:
            attribute = cls._get_column_attribute(name)
            if attribute.default is not None and \
                    not attribute.default.is_sequence and attribute.default.is_scalar:
                result.append(name)

        return tuple(result)

    @class_property
    @fast_cache
    def columns_with_complex_insert_default(cls):
        """
        gets column names that have callable or sequence default values for insert.

        :rtype: tuple[str]
        """

        all_columns = cls.primary_key_columns + cls.all_columns + cls.foreign_key_columns
        result = []
        for name in all_columns:
            attribute = cls._get_column_attribute(name)
            if attribute.default is not None and (attribute.default.is_sequence or
                                                  attribute.default.is_callable):
                result.append(name)

        return tuple(result)

    @class_property
    @fast_cache
    def columns_with_scalar_update_default(cls):
        """
        gets column names that have scalar default values for update.

        :rtype: tuple[str]
        """

        all_columns = cls.all_columns + cls.foreign_key_columns
        result = []
        for name in all_columns:
            attribute = cls._get_column_attribute(name)
            if attribute.onupdate is not None and \
                    not attribute.onupdate.is_sequence and attribute.onupdate.is_scalar:
                result.append(name)

        return tuple(result)

    @class_property
    @fast_cache
    def columns_with_complex_update_default(cls):
        """
        gets column names that have callable or sequence default values for update.

        :rtype: tuple[str]
        """

        all_columns = cls.all_columns + cls.foreign_key_columns
        result = []
        for name in all_columns:
            attribute = cls._get_column_attribute(name)
            if attribute.onupdate is not None and (attribute.onupdate.is_sequence or
                                                   attribute.onupdate.is_callable):
                result.append(name)

        return tuple(result)

    def prefetch_insert_defaults(self, **kwargs):
        """
        prefetches all columns that have default values for insert.

        and their name is not in provided inputs or their value is None.

        :keyword SECURE_TRUE | SECURE_FALSE prefetch_complex_defaults: specifies that all columns
                                                                       that have default values
                                                                       for insert must fetch their
                                                                       default value if no value
                                                                       is provided for them in
                                                                       `kwargs`.
                                                                       note that scalar default
                                                                       values will always be
                                                                       fetched and this option is
                                                                       only for sequence or
                                                                       callable default values.
                                                                       defaults to `SECURE_TRUE`
                                                                       if not provided.

        :note prefetch_complex_defaults: for callable defaults we have to pass
                                         `ExecutionContext` as None because there is no
                                         such context in prefetch time. so if your callable
                                         default actually needs a valid context, you can not
                                         prefetch its value and must disable prefetching by
                                         passing `prefetch_complex_defaults=SECURE_FALSE`.
                                         otherwise unexpected behavior may occur.
        """

        fetch_complex_defaults = kwargs.pop('prefetch_complex_defaults', SECURE_TRUE)
        self._prefetch_insert_defaults(self.columns_with_scalar_insert_default, **kwargs)

        if fetch_complex_defaults is SECURE_TRUE:
            self._prefetch_insert_defaults(self.columns_with_complex_insert_default, **kwargs)

    def _prefetch_insert_defaults(self, columns, **kwargs):
        """
        prefetches all columns that have default values for insert.

        and their name is not in provided inputs or their value is None.

        :param tuple[str] columns: column names that have insert default values.
        """

        for item in columns:
            provided = kwargs.get(item)
            if provided is None:
                self._set_insert_default(item)

    def prefetch_update_defaults(self, **kwargs):
        """
        prefetches all columns that have default values for update.

        and their name is not in provided inputs or their value is None.

        :keyword SECURE_TRUE | SECURE_FALSE prefetch_complex_defaults: specifies that all columns
                                                                       that have default values
                                                                       for update must fetch their
                                                                       default value if no value
                                                                       is provided for them in
                                                                       `kwargs`.
                                                                       note that scalar default
                                                                       values will always be
                                                                       fetched and this option is
                                                                       only for sequence or
                                                                       callable default values.
                                                                       defaults to `SECURE_TRUE`
                                                                       if not provided.

        :note prefetch_complex_defaults: for callable defaults we have to pass
                                         `ExecutionContext` as None because there is no
                                         such context in prefetch time. so if your callable
                                         default actually needs a valid context, you can not
                                         prefetch its value and must disable prefetching by
                                         passing `prefetch_complex_defaults=SECURE_FALSE`.
                                         otherwise unexpected behavior may occur.
        """

        fetch_complex_defaults = kwargs.pop('prefetch_complex_defaults', SECURE_TRUE)
        self._prefetch_update_defaults(self.columns_with_scalar_update_default, **kwargs)

        if fetch_complex_defaults is SECURE_TRUE:
            self._prefetch_update_defaults(self.columns_with_complex_update_default, **kwargs)

    def _prefetch_update_defaults(self, columns, **kwargs):
        """
        prefetches all columns that have default values for update.

        and their name is not in provided inputs or their value is None.

        :param tuple[str] columns: column names that have update default values.
        """

        for item in columns:
            provided = kwargs.get(item)
            if provided is None:
                self._set_update_default(item)

    @classmethod
    def populate_cache(cls):
        """
        populates all related caches.
        """

        temp = cls.columns_with_scalar_insert_default
        temp = cls.columns_with_complex_insert_default
        temp = cls.columns_with_scalar_update_default
        temp = cls.columns_with_complex_update_default
        super().populate_cache()


class OrderingMixin(ModelMixinBase):
    """
    ordering mixin class.

    this class adds functionalities about ordering to its subclasses.
    """

    # a list of entity column instances which are allowed to be used in order by criterion.
    # defaults to all columns of entity if not provided. if set to an empty list ordering
    # will be disabled for all columns.
    # for example:
    # _ordering_columns = None -> allow ordering on all columns (default).
    # _ordering_columns = [] -> disable ordering on all columns.
    # _ordering_columns = name -> allow ordering only on name column.
    # _ordering_columns = age, name, family -> allow ordering on three columns.
    _ordering_columns = None

    @class_property
    @fast_cache
    def ordering_column_names(cls):
        """
        gets all column attribute names which are allowed in order by.

        the result will be calculated once and cached per entity type.

        :raises InvalidOrderingColumnTypeError: invalid ordering column type error.
        :raises ColumnNotExistedError: column not existed error.

        :rtype: tuple[str]
        """

        if cls._ordering_columns is None:
            return cls.all_columns + cls.primary_key_columns + cls.foreign_key_columns

        iterable_columns = misc_utils.make_iterable(cls._ordering_columns, tuple)
        if len(iterable_columns) <= 0:
            return tuple()

        result = []
        for item in iterable_columns:
            if not isinstance(item, CoreColumn):
                raise InvalidOrderingColumnTypeError('Ordering columns on entity [{entity}] '
                                                     'must be an instance of [{column}].'
                                                     .format(entity=cls, column=CoreColumn))

            name = cls.all_reverse_column_attributes.get(item)
            if name is None:
                raise ColumnNotExistedError('Ordering column [{column}] does '
                                            'not exist in entity [{entity}].'
                                            .format(column=item, entity=cls))

            result.append(name)

        return tuple(result)

    @classmethod
    def get_ordering_criterion(cls, *columns, ignore_invalid=True):
        """
        gets required ordering criterion for given column names.

        default ordering is ascending, but it could be changed to descending
        by prefixing `-` to column names.

        for example:

        name, +age -> ordering for name and age columns both ascending.
        name, -age -> ordering for name ascending and age descending.

        :param str columns: column names to get their ordering criterion.
                            they must be the column attribute names of
                            this entity.

        :param bool ignore_invalid: specifies that if provided columns are
                                    not valid, ignore them instead of raising
                                    an error. defaults to True.

        :raises InvalidOrderingColumnError: invalid ordering column error.

        :rtype: tuple[UnaryExpression]
        """

        result = []
        for item in columns:
            if sqlalchemy_utils.is_valid_column_name(item):
                name, order_type = sqlalchemy_utils.get_ordering_info(item)
                attribute = cls._get_column_attribute(name)
                is_allowed = name in cls.ordering_column_names
                if (attribute is None or not is_allowed) and ignore_invalid is False:
                    raise InvalidOrderingColumnError(_('Column [{name}] is not valid '
                                                       'for ordering.').format(name=name))
                elif attribute is not None and is_allowed:
                    result.append(order_type(attribute))

        return tuple(result)

    @classmethod
    def populate_cache(cls):
        """
        populates all related caches.
        """

        temp = cls.ordering_column_names
        super().populate_cache()


class CreateHistoryMixin:
    """
    create history mixin class.

    this class adds `created_on` column into its subclasses.
    """

    created_on = TimeStampColumn(name='created_on', nullable=False, validated=True,
                                 validated_find=False, validated_range=True,
                                 default=datetime_services.now, allow_write=False)


class UpdateHistoryMixin:
    """
    update history mixin class.

    this class adds `modified_on` column into its subclasses.
    """

    modified_on = TimeStampColumn(name='modified_on', nullable=True, validated=True,
                                  validated_find=False, validated_range=True,
                                  onupdate=datetime_services.now, allow_write=False)


class HistoryMixin(CreateHistoryMixin, UpdateHistoryMixin):
    """
    history mixin class.

    this class adds `created_on` and `modified_on` columns into its subclasses.
    """
    pass
