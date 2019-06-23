# -*- coding: utf-8 -*-
"""
database manager module.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

import pyrin.configuration.services as config_services

from pyrin.core.context import CoreObject


class DatabaseManager(CoreObject):
    """
    database manager class.
    """

    def __init__(self):
        """
        initializes an instance of DatabaseManager.
        """

        CoreObject.__init__(self)

        db_connection = config_services.get_active('database', 'sqlalchemy_database_uri')
        self._engine = create_engine(db_connection, echo=True)
        self._session = scoped_session(sessionmaker(autocommit=False, bind=self._engine))

    def get_current_session(self):
        """
        gets current database session.

        :returns: database session
        """

        return self._session
