# -*- coding: utf-8 -*-
"""
database base module.
"""

from sqlalchemy.exc import DatabaseError
from sqlalchemy.ext.declarative import declarative_base

import pyrin.database.services as database_services

from pyrin.core.context import CoreObject
from pyrin.database.exceptions import DatabaseOperationError


class CoreDeclarative(CoreObject):
    """
    core declarative class.
    it will be used to create a declarative base for all models.
    """

    def save(self):
        """
        saves the current entity.

        :raises DatabaseOperationError: database operation error.
        """

        database_services.get_current_session().add(self)
        self._flush()
        return self

    def update(self, **kwargs):
        """
        updates the current entity with given values.

        :raises DatabaseOperationError: database operation error.
        """

        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return self.save()

    def delete(self):
        """
        deletes the current entity.

        :raises DatabaseOperationError: database operation error.
        """

        database_services.get_current_session().delete(self)
        self._flush()

    def _flush(self):
        """
        flushes the instructions into database but not committing.

        :raises DatabaseOperationError: database operation error.
        """

        try:
            database_services.get_current_session().flush()
        except DatabaseError as error:
            database_services.get_current_session().rollback()
            raise DatabaseOperationError(error) from error


# this entity should be used as the base entity for all application entities.
CoreEntity = declarative_base(cls=CoreDeclarative)
CoreEntity.query = database_services.get_current_session().query_property()
