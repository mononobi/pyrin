# -*- coding: utf-8 -*-
"""
database manager module.
"""

from sqlalchemy import engine_from_config
from sqlalchemy.orm import scoped_session, sessionmaker

import pyrin.configuration.services as config_services
import pyrin.security.session.services as session_services

from pyrin.core.context import CoreObject


class DatabaseManager(CoreObject):
    """
    database manager class.
    """

    _CONFIGS_PREFIX = 'sqlalchemy_'

    def __init__(self):
        """
        initializes an instance of DatabaseManager.
        """

        CoreObject.__init__(self)

        self.__engine = self._create_engine()
        self.__session_factory = self._create_scoped_session_factory()

    def get_current_store(self):
        """
        gets current database store.

        :returns: database session
        :rtype: Session
        """

        return self.__session_factory()

    def get_session_factory(self):
        """
        gets database session factory.
        this method should not be used directly for data manipulation.
        use `get_current_store` method instead.

        :returns: database session factory
        :rtype: Session
        """

        return self.__session_factory

    def _create_engine(self):
        """
        creates a database engine using database configuration store and returns it.

        :returns: database engine.
        :rtype: Engine
        """

        database_configs = config_services.get_active_section('database')
        return engine_from_config(database_configs, prefix=self._CONFIGS_PREFIX)

    def _create_scoped_session_factory(self):
        """
        creates a database scoped session factory and binds it to
        current engine and returns it.
        the scope is current request, so each request will get
        it's own session from start to end.

        :returns: database session
        :rtype: Session
        """

        session_configs = config_services.get_section('database', 'session')
        return scoped_session(sessionmaker(bind=self.__engine, **session_configs),
                              scopefunc=session_services.get_current_request)
