# -*- coding: utf-8 -*-
"""
model base module.
"""

import inspect

from sqlalchemy import inspect as sqla_inspect
from sqlalchemy.ext.declarative import as_declarative

import pyrin.database.services as database_services

from pyrin.core.context import CoreObject, DTO
from pyrin.database.model.exceptions import ColumnNotExistedError


@as_declarative(constructor=None)
class CoreEntity(CoreObject):
    """
    core entity class.

    it should be used as the base class for all application models.

    it is also possible to implement a new customized base class for your application
    models. to do this you could subclass from every needed mixin class of `model.mixins`
    and also implement your customized or new features. keep in mind that you could not
    subclass directly from `CoreEntity`, because it has `@as_declarative` decorator
    and sqlalchemy raises an error if you subclass from this as your new base model.
    """

    # holds the table name in database.
    __tablename__ = None

    # holds the extra arguments for table.
    # for example:
    # __table_args__ = {'schema': 'database_name.schema_name',
    #                   'extend_existing': True}
    __table_args__ = None

    def __init__(self, *args, **kwargs):
        """
        initializes an instance of CoreEntity.

        note that this method will only be called on user code, meaning
        that results returned by orm from database will not call `__init__`
        of each entity.

        it also could set attributes on the constructed instance using the
        names and values in `kwargs`. all keys that are present as either mapped
        columns or relationship properties of the instance's class are allowed.

        :raises ColumnNotExistedError: column not existed error.
        """

        super().__init__()

        self._set_name(self.__class__.__name__)
        self.from_dict(False, **kwargs)

    def __eq__(self, other):
        if isinstance(other, self._get_root_base_class()):
            if self._is_primary_key_comparable(self.primary_key()) is True:
                return self.primary_key() == other.primary_key()
            else:
                return self is other

        return False

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        if self._is_primary_key_comparable(self.primary_key()) is True:
            return hash('{root_base}.{pk}'.format(root_base=self._get_root_base_class(),
                                                  pk=self.primary_key()))
        return super().__hash__()

    def __repr__(self):
        """
        gets the string representation of current entity.

        :rtype: str
        """
        return '{module}.{name} [{pk}]'.format(module=self.__module__,
                                               name=self.get_name(),
                                               pk=self.primary_key())

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

    def _get_root_base_class(self):
        """
        gets root base class of this entity and caches it.

        root base class is the class which is direct subclass
        of CoreEntity in inheritance hierarchy.
        for example: {Base -> CoreEntity, A -> Base, B -> A}
        root base class of A, B and Base is Base class.

        :rtype: type
        """

        base = getattr(self, '_root_base_class', None)
        if base is None:
            bases = inspect.getmro(type(self))
            base_entity_index = bases.index(CoreEntity) - 1
            base = bases[base_entity_index]
            self.__class__._root_base_class = base

        return base

    def _set_all_columns(self, columns):
        """
        sets all column names attribute for this class.

        :param tuple[str] columns: column names.
        """

        if getattr(self, '_all_columns', None) is None:
            self.__class__._all_columns = DTO()

        self.__class__._all_columns[type(self)] = columns

    def _set_exposed_columns(self, columns):
        """
        sets exposed column names attribute for this class.

        :param tuple[str] columns: column names.
        """

        if getattr(self, '_exposed_columns', None) is None:
            self.__class__._exposed_columns = DTO()

        self.__class__._exposed_columns[type(self)] = columns

    def _set_relationships(self, relationships):
        """
        sets relationship property names attribute for this class.

        :param tuple[str] relationships: relationship property names.
        """

        if getattr(self, '_relationships', None) is None:
            self.__class__._relationships = DTO()

        self.__class__._relationships[type(self)] = relationships

    def _set_all_columns_and_relationships(self, all_properties):
        """
        sets all column and relationship property names attribute for this class.

        :param tuple[str] all_properties: all property names.
        """

        if getattr(self, '_all_columns_and_relationships', None) is None:
            self.__class__._all_columns_and_relationships = DTO()

        self.__class__._all_columns_and_relationships[type(self)] = all_properties

    def _set_exposed_columns_and_relationships(self, exposed_properties):
        """
        sets exposed column and relationship property names attribute for this class.

        exposed columns are those that have `exposed=True` in their definition.

        :param tuple[str] exposed_properties: exposed property names.
        """

        if getattr(self, '_exposed_columns_and_relationships', None) is None:
            self.__class__._exposed_columns_and_relationships = DTO()

        self.__class__._exposed_columns_and_relationships[type(self)] = exposed_properties

    def _set_primary_key_columns(self, columns):
        """
        sets primary key column names attribute for this class.

        :param tuple[str] columns: column names.
        """

        if getattr(self, '_primary_key_columns', None) is None:
            self.__class__._primary_key_columns = DTO()

        self.__class__._primary_key_columns[type(self)] = columns

    def save(self):
        """
        saves the current entity.
        """

        database_services.get_current_store().add(self)
        return self

    def update(self, **kwargs):
        """
        updates the current entity with given values.
        """

        self.from_dict(**kwargs)
        return self.save()

    def delete(self):
        """
        deletes the current entity.
        """

        database_services.get_current_store().delete(self)

    def _get_primary_keys(self):
        """
        gets current entity's primary key column names if available.

        :rtype: tuple[str]
        """

        columns = getattr(self, '_primary_key_columns', None)
        if columns is not None:
            return columns.get(type(self), None)

        return None

    @property
    def primary_key_columns(self):
        """
        gets the primary key column names of this entity.

        column names will be calculated once and cached.

        :rtype: tuple[str]
        """

        pk = self._get_primary_keys()
        if pk is None:
            info = sqla_inspect(type(self))
            pk = tuple(info.get_property_by_column(col).key for col in info.primary_key)
            self._set_primary_key_columns(pk)

        return pk

    @property
    def all_columns(self):
        """
        gets all column names of this entity.

        column names will be calculated once and cached.

        :rtype: tuple[str]
        """

        columns = self._get_all_columns()
        if columns is None:
            info = sqla_inspect(type(self))
            columns = tuple(attr.key for attr in info.column_attrs)
            self._set_all_columns(columns)

        return columns

    @property
    def exposed_columns(self):
        """
        gets exposed column names of this entity, which are those that have `exposed=True`.

        column names will be calculated once and cached.

        :rtype: tuple[str]
        """

        columns = self._get_exposed_columns()
        if columns is None:
            info = sqla_inspect(type(self))
            columns = tuple(attr.key for attr in info.column_attrs
                            if attr.columns[0].exposed is True)
            self._set_exposed_columns(columns)

        return columns

    @property
    def relationships(self):
        """
        gets all relationship property names of this entity.

        property names will be calculated once and cached.

        :rtype: tuple[str]
        """

        relationships = self._get_relationships()
        if relationships is None:
            info = sqla_inspect(type(self))
            relationships = tuple(attr.key for attr in info.relationships)
            self._set_relationships(relationships)

        return relationships

    @property
    def all_columns_and_relationships(self):
        """
        gets all column and relationship property names of this entity.

        property names will be calculated once and cached.

        :rtype: tuple[str]
        """

        all_properties = self._get_all_columns_and_relationships()
        if all_properties is None:
            all_properties = self.all_columns + self.relationships
            self._set_all_columns_and_relationships(all_properties)

        return all_properties

    @property
    def exposed_columns_and_relationships(self):
        """
        gets exposed column and relationship property names of this entity.

        exposed columns are those that have `exposed=True` is their definition.
        property names will be calculated once and cached.

        :rtype: tuple[str]
        """

        exposed_properties = self._get_exposed_columns_and_relationships()
        if exposed_properties is None:
            exposed_properties = self.exposed_columns + self.relationships
            self._set_exposed_columns_and_relationships(exposed_properties)

        return exposed_properties

    def _get_all_columns(self):
        """
        gets all column names of this entity.

        returns None if not found.

        :rtype: tuple[str]
        """

        columns = getattr(self, '_all_columns', None)
        if columns is not None:
            return columns.get(type(self), None)

        return None

    def _get_exposed_columns(self):
        """
        gets exposed column names of this entity, which are those that have `exposed=True`.

        returns None if not found.

        :rtype: tuple[str]
        """

        columns = getattr(self, '_exposed_columns', None)
        if columns is not None:
            return columns.get(type(self), None)

        return None

    def _get_relationships(self):
        """
        gets all relationship property names of this entity.

        returns None if not found.

        :rtype: tuple[str]
        """

        relationships = getattr(self, '_relationships', None)
        if relationships is not None:
            return relationships.get(type(self), None)

        return None

    def _get_all_columns_and_relationships(self):
        """
        gets all column and relationship property names of this entity.

        returns None if not found.

        :rtype: tuple[str]
        """

        all_properties = getattr(self, '_all_columns_and_relationships', None)
        if all_properties is not None:
            return all_properties.get(type(self), None)

        return None

    def _get_exposed_columns_and_relationships(self):
        """
        gets exposed column and relationship property names of this entity.

        returns None if not found.

        :rtype: tuple[str]
        """

        exposed_properties = getattr(self, '_exposed_columns_and_relationships', None)
        if exposed_properties is not None:
            return exposed_properties.get(type(self), None)

        return None

    def to_dict(self, exposed_only=True, **options):
        """
        converts the entity into a dict and returns it.

        the result dict only contains the exposed columns of
        the entity which are those that their `exposed` attribute
        is set to True.

        :param bool exposed_only: if set to False, it returns all
                                  columns of the entity as dict.
                                  if not provided, defaults to True.

        :keyword list[str] columns: the column names to be included in result.
                                    if not provided, the columns in exposed
                                    columns or all columns will be returned.
                                    note that the columns must be a subset of
                                    all columns or exposed columns of this
                                    entity considering "exposed_only" parameter,
                                    otherwise it raises an error.

        :raises ColumnNotExistedError: column not existed error.

        :rtype: dict
        """

        base_columns = None
        requested_columns = options.get('columns', None)

        if exposed_only is False:
            base_columns = self.all_columns
        else:
            base_columns = self.exposed_columns

        result = DTO()
        if requested_columns is None or len(requested_columns) <= 0:
            requested_columns = base_columns

        difference = set(requested_columns).difference(set(base_columns))
        if len(difference) > 0:
            raise ColumnNotExistedError('Requested columns {columns} are '
                                        'not available in entity [{entity}].'
                                        'it might be because of "exposed_only" '
                                        'parameter value passed to this method.'
                                        .format(columns=list(difference), entity=self))
        for col in requested_columns:
            result[col] = getattr(self, col)

        return result

    def from_dict(self, silent_on_invalid_column=True, **kwargs):
        """
        updates the column values of this entity with values in keyword arguments.

        it could fill columns and also relationship properties if provided.

        :keyword bool silent_on_invalid_column: specifies that if a key is not available
                                                in entity columns, do not raise an error.
                                                defaults to True if not provided.

        :raises ColumnNotExistedError: column not existed error.
        """

        all_properties = self.all_columns_and_relationships
        for key, value in kwargs.items():
            if key in all_properties:
                setattr(self, key, value)
            else:
                if silent_on_invalid_column is False:
                    raise ColumnNotExistedError('Entity [{entity}] does not have '
                                                'a column or relationship attribute '
                                                'named [{column}].'
                                                .format(entity=self,
                                                        column=key))

    @classmethod
    def table_name(cls):
        """
        gets the table name that this entity represents in database.

        :rtype: str
        """

        return cls.__tablename__

    @classmethod
    def table_schema(cls):
        """
        gets the table schema that this entity represents in database.

        it might be `None` if schema has not been set for this entity.

        :rtype: str
        """

        schema = None
        if cls.__table_args__ is not None:
            schema = cls.__table_args__.get('schema', None)

        return schema

    @classmethod
    def table_fullname(cls):
        """
        gets the table fullname that this entity represents in database.

        fullname is `schema.table_name` if schema is available, otherwise it
        defaults to `table_name`.

        :rtype: str
        """

        schema = cls.table_schema()
        name = cls.table_name()

        if schema is not None:
            return '{schema}.{name}'.format(schema=schema, name=name)
        else:
            return name
