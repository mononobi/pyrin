# -*- coding: utf-8 -*-
"""
model base module.
"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import class_mapper, ColumnProperty

import pyrin.database.services as database_services
import pyrin.database.sequence.services as sequence_services

from pyrin.core.context import CoreObject, DTO
from pyrin.database.model.exceptions import SequenceHasNotSetError


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

    def __init__(self):
        """
        initializes an instance of CoreDeclarative.
        """

        CoreObject.__init__(self)

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
                                         .format(name=self.__class__.__name__))

        return sequence_services.get_next_value(self.__primary_key_sequence__)

    def all_columns(self):
        """
        gets all column names of entity.

        :returns: list[str]
        :rtype: list
        """

        all_columns = [prop.key for prop in class_mapper(type(self)).iterate_properties
                       if isinstance(prop, ColumnProperty)]

        return all_columns

    def exposed_columns(self):
        """
        gets exposed column names of entity, which
        are those that have `hidden=False`.

        :returns: list[str]
        :rtype: list
        """

        all_columns = [prop.key for prop in class_mapper(type(self)).iterate_properties
                       if isinstance(prop, ColumnProperty) and prop.columns[0].hidden is False]

        return all_columns

    def to_dict(self):
        """
        converts the entity into a dict and returns it.
        the result dict only contains the exposed columns of
        the entity which are those that their `hidden` attribute
        is set to False.

        :rtype: dict
        """

        result = DTO()
        for col in self.exposed_columns():
            result[col] = self.__dict__[col]

        return result

    def from_dict(self, **kwargs):
        """
        updates the column values of the entity from those
        values that are available in input keyword arguments.
        """

        all_columns = self.all_columns()
        for key, value in kwargs.items():
            if key in all_columns:
                setattr(self, key, value)


# this entity should be used as the base entity for all application entities.
CoreEntity = declarative_base(cls=CoreDeclarative, name='CoreEntity')
