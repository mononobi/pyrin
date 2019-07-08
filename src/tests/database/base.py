# -*- coding: utf-8 -*-
"""
database base module.
"""

from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.declarative import declarative_base

import pyrin.database.services as database_services

from pyrin.core.context import CoreObject


class CoreDeclarative(CoreObject):
    """
    core declarative class.
    it will be used to create a declarative base for all models.
    """

    # holds the table name in database.
    __tablename__ = None

    # holds all foreign keys of current table. it should be in the following patterns.
    # (current_table.id, reference_table.id)
    # (current_table.name, reference_table.name), (current_table.desc, reference_table.desc)
    __foreign_key__ = None

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

    def _flush(self):
        """
        flushes the instructions into database but not committing.

        :raises DatabaseOperationError: database operation error.
        """

        store = database_services.get_current_store()
        try:
            store.flush()
        except DatabaseError as error:
            store.rollback()
            raise error


# this entity should be used as the base entity for all application entities.
CoreEntity = declarative_base(cls=CoreDeclarative)
CoreEntity.query = database_services.get_session_factory().query_property()
