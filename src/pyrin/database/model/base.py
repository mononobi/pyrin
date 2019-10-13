# -*- coding: utf-8 -*-
"""
model base module.
"""

from sqlalchemy.ext.declarative import declarative_base

import pyrin.database.services as database_services
import pyrin.database.sequence.services as sequence_services

from pyrin.core.context import CoreObject
from pyrin.database.model.exceptions import SequenceHasNotSetError


class CoreDeclarative(CoreObject):
    """
    core declarative class.
    it will be used to create a declarative base for all models.
    """

    # holds the table name in database.
    __tablename__ = None

    # holds the extra arguments for table.
    __table_args__ = None

    # holds all foreign keys of current table. it should be in the following patterns.
    # (current_table.id, reference_table.id)
    # (current_table.name, reference_table.name), (current_table.desc, reference_table.desc)
    __foreign_key__ = None

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

        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return self.save()

    def delete(self):
        """
        deletes the current entity.
        """

        database_services.get_current_store().delete(self)

    def get_new_primary_key(self):
        """
        gets a new primary key using `__primary_key_sequence__` value.

        :raises SequenceHasNotSetError: sequence has not set error.

        :rtype: int
        """

        if self.__primary_key_sequence__ in (None, ''):
            raise SequenceHasNotSetError('No primary key sequence has been set '
                                         'for table [{table}].'.format(table=self.__tablename__))

        return sequence_services.get_next_value(self.__primary_key_sequence__)


# this entity should be used as the base entity for all application entities.
CoreEntity = declarative_base(cls=CoreDeclarative)

# TODO: the below line must be removed completely so everyone forced to
#  query on objects from store itself, not from the model.
CoreEntity.query = database_services.get_session_factory(request_bounded=True).query_property()
