# -*- coding: utf-8 -*-
"""
model base module.
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper, ColumnProperty

import pyrin.database.services as database_services
import pyrin.database.sequence.services as sequence_services

from pyrin.core.context import CoreObject, DTO
from pyrin.database.model.exceptions import SequenceHasNotSetError, ColumnNotExistedError


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

    # holds the name of the sequence used for table's primary key column.
    __primary_key_sequence__ = None

    def __init__(self, *args, **kwargs):
        """
        initializes an instance of CoreDeclarative.
        note that this method will only be called on user code, meaning
        that results returned by orm from database will not call `__init__`
        of each entity.

        :raises ColumnNotExistedError: column not existed error.
        """

        CoreObject.__init__(self)

        if not hasattr(self, '_all_columns'):
            self._set_all_columns(None)

        if not hasattr(self, '_exposed_columns'):
            self._set_exposed_columns(None)

        self._set_name(self.__class__.__name__)
        self.from_dict(False, **kwargs)

    def _set_all_columns(self, columns):
        """
        sets all column names attribute for this class.

        :param tuple[str] columns: column names.
        """

        self.__class__._all_columns = columns

    def _set_exposed_columns(self, columns):
        """
        sets exposed column names attribute for this class.

        :param tuple[str] columns: column names.
        """

        self.__class__._exposed_columns = columns

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

    def new_primary_key(self):
        """
        gets a new primary key using `__primary_key_sequence__` value.

        :raises SequenceHasNotSetError: sequence has not set error.

        :rtype: int
        """

        if self.__primary_key_sequence__ in (None, ''):
            raise SequenceHasNotSetError('No primary key sequence has been set '
                                         'for entity [{name}].'
                                         .format(name=self.get_name()))

        return sequence_services.get_next_value(self.__primary_key_sequence__)

    def all_columns(self):
        """
        gets all column names of entity.
        column names will be calculated once and cached.

        :returns: tuple[str]
        :rtype: tuple
        """

        if self._all_columns is None:
            all_columns = tuple(prop.key for prop in class_mapper(type(self)).iterate_properties
                                if isinstance(prop, ColumnProperty))
            self._set_all_columns(all_columns)

        return self._all_columns

    def exposed_columns(self):
        """
        gets exposed column names of entity, which
        are those that have `exposed=True`.
        column names will be calculated once and cached.

        :returns: tuple[str]
        :rtype: tuple
        """

        if self._exposed_columns is None:
            exposed_columns = tuple(prop.key for prop in class_mapper(type(self)).
                                    iterate_properties if isinstance(prop, ColumnProperty)
                                    and prop.columns[0].exposed is True)
            self._set_exposed_columns(exposed_columns)

        return self._exposed_columns

    def to_dict(self):
        """
        converts the entity into a dict and returns it.
        the result dict only contains the exposed columns of
        the entity which are those that their `exposed` attribute
        is set to True.

        :rtype: dict
        """

        result = DTO()
        for col in self.exposed_columns():
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


# this entity should be used as the base entity for all application entities.
CoreEntity = declarative_base(cls=CoreDeclarative, name='CoreEntity', constructor=None)
