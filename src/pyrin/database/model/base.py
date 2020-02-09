# -*- coding: utf-8 -*-
"""
model base module.
"""

import inspect

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper, ColumnProperty

import pyrin.database.services as database_services

from pyrin.core.context import CoreObject, DTO
from pyrin.database.model.exceptions import ColumnNotExistedError, EntityNotHashableError


class CoreDeclarative(CoreObject):
    """
    core declarative class.
    it will be used to create a declarative base for all models.
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
        initializes an instance of CoreDeclarative.
        note that this method will only be called on user code, meaning
        that results returned by orm from database will not call `__init__`
        of each entity.

        it also sets attributes on the constructed instance using the
        names and values in `kwargs`. note that only keys that are present
        as mapped columns of the instance's class are allowed.

        :raises ColumnNotExistedError: column not existed error.
        """

        super().__init__()

        self._set_name(self.__class__.__name__)
        self.from_dict(False, **kwargs)

    def __eq__(self, other):
        if isinstance(other, self._get_root_base_class()):
            if self.primary_key() is not None:
                return self.primary_key() == other.primary_key()
            else:
                return self is other

        return False

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        if self.primary_key() is None:
            raise EntityNotHashableError('Entity [{entity}] does not have '
                                         'a primary key so it is not hashable.'
                                         .format(entity=self.get_name()))

        return hash('{root_base}.{pk}'.format(root_base=self._get_root_base_class(),
                                              pk=self.primary_key()))

    def __repr__(self):
        return '<{module}.{name} [{pk}]>'.format(module=self.__module__,
                                                 name=self.get_name(),
                                                 pk=str(self.primary_key()))

    def __str__(self):
        return str(self.primary_key())

    def _get_root_base_class(self):
        """
        gets root base class of this entity and caches it.
        root base class is the class which is direct subclass
        of CoreEntity in inheritance hierarchy.
        for example: {Base -> CoreEntity, A -> Base, B -> A}
        root base class of A, B and Base is Base class.

        :rtype: CoreEntity
        """

        if getattr(self, '_root_base_class', None) is None:
            bases = inspect.getmro(type(self))
            base_entity_index = bases.index(CoreEntity) - 1
            self.__class__._root_base_class = bases[base_entity_index]

        return self.__class__._root_base_class

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

    def primary_key(self):
        """
        gets the primary key value of this entity.

        note that the returning value of this method will be used as a way
        to compare two different entities of the same type. so if your table
        does not have a primary key, you could either not implement this method
        and leave comparison to base in the form of `self is other` or you could
        implement another logic in this method to make comparisons possible and
        correct. the returning value of this method must be hashable.

        :rtype: object
        """

        return None

    def all_columns(self):
        """
        gets all column names of entity.
        column names will be calculated once and cached.

        :returns: tuple[str]
        :rtype: tuple
        """

        columns = self._get_all_columns()
        if columns is None:
            all_columns = tuple(prop.key for prop in class_mapper(type(self)).iterate_properties
                                if isinstance(prop, ColumnProperty))
            self._set_all_columns(all_columns)

        return self._get_all_columns()

    def exposed_columns(self):
        """
        gets exposed column names of entity, which
        are those that have `exposed=True`.
        column names will be calculated once and cached.

        :returns: tuple[str]
        :rtype: tuple
        """

        columns = self._get_exposed_columns()
        if columns is None:
            exposed_columns = tuple(prop.key for prop in class_mapper(type(self)).
                                    iterate_properties if isinstance(prop, ColumnProperty)
                                    and prop.columns[0].exposed is True)
            self._set_exposed_columns(exposed_columns)

        return self._get_exposed_columns()

    def _get_all_columns(self):
        """
        gets all column names of entity.
        returns None if not found.

        :returns: tuple[str]
        :rtype: tuple
        """

        columns = getattr(self, '_all_columns', None)
        if columns is not None:
            return columns.get(type(self), None)

        return None

    def _get_exposed_columns(self):
        """
        gets exposed column names of entity, which
        are those that have `exposed=True`.
        returns None if not found.

        :returns: tuple[str]
        :rtype: tuple
        """

        columns = getattr(self, '_exposed_columns', None)
        if columns is not None:
            return columns.get(type(self), None)

        return None

    def to_dict(self, exposed_only=True):
        """
        converts the entity into a dict and returns it.
        the result dict only contains the exposed columns of
        the entity which are those that their `exposed` attribute
        is set to True.

        :param bool exposed_only: if set to False, it returns all
                                  columns of the entity as dict.
                                  if not provided, defaults to True.

        :rtype: dict
        """

        columns_collection = self.exposed_columns
        if exposed_only is False:
            columns_collection = self.all_columns

        result = DTO()
        for col in columns_collection():
            result[col] = getattr(self, col)

        return result

    def from_dict(self, silent_on_invalid_column=True, **kwargs):
        """
        updates the column values of the entity from those
        values that are available in input keyword arguments.

        :keyword bool silent_on_invalid_column: specifies that if a key is not available
                                                in entity columns, do not raise an error.
                                                defaults to True if not provided.

        :raises ColumnNotExistedError: column not existed error.
        """

        all_columns = self.all_columns()
        for key, value in kwargs.items():
            if key in all_columns:
                setattr(self, key, value)
            else:
                if silent_on_invalid_column is False:
                    raise ColumnNotExistedError('Entity [{entity}] does not have '
                                                'a column named [{column}].'
                                                .format(entity=self.get_name(),
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
        it might be an empty string if schema has not been set for this entity.

        :rtype: str
        """

        schema = ''
        if cls.__table_args__ is not None:
            schema = cls.__table_args__.get('schema', '')

        return schema.strip()

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

        if schema not in (None, '') and not schema.isspace():
            return '{schema}.{name}'.format(schema=schema, name=name)
        else:
            return name


# this entity should be used as the base entity for all application entities.
CoreEntity = declarative_base(cls=CoreDeclarative, name='CoreEntity', constructor=None)
