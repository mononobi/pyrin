# -*- coding: utf-8 -*-
"""
database manager module.
"""

from sqlalchemy.exc import DatabaseError
from sqlalchemy import engine_from_config
from sqlalchemy.orm import scoped_session, sessionmaker

import pyrin.configuration.services as config_services
import pyrin.database.services as database_services
import pyrin.logging.services as logging_services
import pyrin.security.session.services as session_services

from pyrin.core.context import CoreObject
from pyrin.core.enumerations import ClientErrorResponseCodeEnum, ServerErrorResponseCodeEnum
from pyrin.utils import response as response_utils


class DatabaseManager(CoreObject):
    """
    database manager class.
    """

    LOGGER = logging_services.get_logger('database')
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

        :returns: database engine
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

    def finalize_transaction(self, response):
        """
        this method will finalize database transaction of each request.
        we should not raise any exception in request handlers, so we return
        an error response in case of any exception.
        note that normally you should never call this method manually.

        :param CoreResponse response: response object.

        :rtype: CoreResponse
        """

        client_request = None
        try:
            client_request = session_services.get_current_request()
            store = database_services.get_current_store()
            session_factory = database_services.get_session_factory()
            try:
                if response.status_code >= ClientErrorResponseCodeEnum.BAD_REQUEST:
                    store.rollback()
                    return response

                store.commit()
                return response
            except DatabaseError as error:
                store.rollback()
                raise error
            finally:
                session_factory.remove()
        except Exception as error:
            self.LOGGER.exception(str(error))
            return response_utils.make_exception_response(error,
                                                          code=ServerErrorResponseCodeEnum.
                                                          INTERNAL_SERVER_ERROR)

    def cleanup_session(self, exception):
        """
        this method will cleanup database session of each request in
        case of any unhandled exception. we should not raise any exception
        in teardown request handlers, so we just log the exception.
        note that normally you should never call this method manually.

        :param Exception exception: exception instance.
        """

        if exception is not None:
            try:
                session_factory = database_services.get_session_factory()
                session_factory.remove()
                self.LOGGER.exception(str(exception))

            except Exception as error:
                self.LOGGER.exception(str(error))
