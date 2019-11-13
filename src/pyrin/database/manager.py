# -*- coding: utf-8 -*-
"""
database manager module.
"""

from sqlalchemy.exc import DatabaseError
from sqlalchemy import engine_from_config

import pyrin.configuration.services as config_services
import pyrin.database.services as database_services
import pyrin.logging.services as logging_services
import pyrin.security.session.services as session_services

from pyrin.core.context import CoreObject, DTO
from pyrin.core.enumerations import ClientErrorResponseCodeEnum, ServerErrorResponseCodeEnum
from pyrin.database.session_factory.base import SessionFactoryBase
from pyrin.utils import response as response_utils
from pyrin.utils.custom_print import print_warning
from pyrin.database.exceptions import InvalidSessionFactoryTypeError, \
    DuplicatedSessionFactoryError, SessionFactoryNotExistedError, InvalidEntityTypeError, \
    InvalidDatabaseBindError


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

        # contains the application default database engine.
        self.__engine = self._create_default_engine()

        # a dictionary containing engines for different bounded databases.
        # in the form of: {str bind_name: Engine engine}
        self.__bounded_engines = self._create_bounded_engines()

        # a dictionary containing all entity classes that should be bounded
        # into a database other than the default one.
        # in the form of: {type entity: str bind_name}
        self._binds = DTO()

        # a dictionary containing all entity types that are bounded to a
        # different database than the default one.
        # in the form of: {type entity: Engine engine}
        self._entity_to_engine_map = DTO()

        # a dictionary containing session factories for request bounded and unbounded types.
        # in the for of: {bool request_bounded: Session session_factory}
        # it should have at most two different keys, True for request bounded
        # and False for request unbounded.
        self._session_factories = DTO()

    def get_current_store(self):
        """
        gets current database store.

        :returns: database session
        :rtype: Session
        """

        return self._get_current_session_factory()()

    def get_session_factory(self, request_bounded=None):
        """
        gets database session factory based on given input.
        this method should not be used directly for data manipulation.
        use `get_current_store` method instead.

        :param bool request_bounded: a value indicating that the session
                                     factory should be bounded into request.
                                     if not provided, it gets the current
                                     valid session factory.

        :returns: database session factory
        :rtype: Session
        """

        if request_bounded is None:
            return self._get_current_session_factory()

        return self._get_session_factory(request_bounded)

    def _get_current_session_factory(self):
        """
        gets database session factory that should be used.
        it simply checks that request is available in current
        context or not, and gets the correct session factory.

        :returns: database session factory
        :rtype: Session
        """

        return self._get_session_factory(session_services.is_request_context_available())

    def _get_session_factory(self, request_bounded):
        """
        gets the session factory based on given input.

        :param bool request_bounded: a value indicating that the session
                                     factory should be bounded into request.

        :raises SessionFactoryNotExistedError: session factory not existed error.

        :returns: database session factory
        :rtype: Session
        """

        if request_bounded not in self._session_factories.keys():
            raise SessionFactoryNotExistedError('Session factory with '
                                                'request_bounded={bounded} '
                                                'is not available.'
                                                .format(bounded=request_bounded))

        return self._session_factories.get(request_bounded)

    def _create_default_engine(self):
        """
        creates the default database engine using database
        configuration store and returns it.

        :returns: database engine
        :rtype: Engine
        """

        database_configs = config_services.get_active_section('database')
        return self._create_engine(database_configs)

    def _create_engine(self, database_configs, **kwargs):
        """
        creates a database engine using specified database configuration and returns it.
        each provided key from kwargs will override the corresponding
        key in database_configs dict. note that kwargs should not have any prefix.

        :param dict database_configs: database configs that should be used.

        :returns: database engine
        :rtype: Engine
        """

        return engine_from_config(database_configs, prefix=self._CONFIGS_PREFIX, **kwargs)

    def _create_bounded_engines(self):
        """
        creates all required bounded engines if any and returns them.

        :returns: dict(str bind_name: Engine engine)
        :rtype: dict(str, Engine)
        """

        engines = DTO()
        base_database_configs = config_services.get_active_section('database')
        binds = config_services.get_active_section('database.binds')

        if len(binds) <= 0:
            return engines

        for key in binds.keys():
            engine = self._create_engine(base_database_configs, url=binds[key])
            engines[key] = engine

        return engines

    def finalize_transaction(self, response):
        """
        this method will finalize database transaction of each request.
        we should not raise any exception in request handlers, so we return
        an error response in case of any exception.
        note that normally you should never call this method manually.

        :param CoreResponse response: response object.

        :rtype: CoreResponse
        """

        try:
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

    def register_session_factory(self, instance, **options):
        """
        registers a new session factory or replaces the existing one
        if `replace=True` is provided. otherwise, it raises an error
        on adding an instance which it's is_request_bounded() is already available
        in registered session factories.

        :param SessionFactoryBase instance: session factory to be registered.
                                            it must be an instance of SessionFactoryBase.

        :keyword bool replace: specifies that if there is another registered
                               session factory with the same is_request_bounded(),
                               replace it with the new one, otherwise raise an error.
                               defaults to False.

        :raises InvalidSessionFactoryTypeError: invalid session factory type error.
        :raises DuplicatedSessionFactoryError: duplicated session factory error.
        """

        if not isinstance(instance, SessionFactoryBase):
            raise InvalidSessionFactoryTypeError('Input parameter [{instance}] is '
                                                 'not an instance of SessionFactoryBase.'
                                                 .format(instance=str(instance)))

        # checking whether is there any registered instance with the same name.
        if instance.is_request_bounded() in self._session_factories.keys():
            replace = options.get('replace', False)

            if replace is not True:
                raise DuplicatedSessionFactoryError('There is another registered session factory '
                                                    'with "is_request_bounded={bounded}" but '
                                                    '"replace" option is not set, so session '
                                                    'factory [{instance}] could not be registered.'
                                                    .format(bounded=instance.is_request_bounded(),
                                                            instance=str(instance)))

            old_instance = self._session_factories[instance.is_request_bounded()]
            print_warning('Session factory [{old_instance}] is going '
                          'to be replaced by [{new_instance}].'
                          .format(old_instance=str(old_instance), new_instance=str(instance)))

        # registering new session factory.
        self._session_factories[instance.is_request_bounded()] = \
            instance.create_session_factory(self.__engine)

    def register_bind(self, cls, bind_name, **options):
        """
        binds the given model class with specified bind database.

        :param CoreEntity cls: CoreEntity subclass to be bounded.
        :param str bind_name: bind name to be associated with the model class.

        :raises InvalidEntityTypeError: invalid entity type error.
        """

        # we have to import CoreEntity inside this method to
        # prevent early access to database.services before being available.
        from pyrin.database.model.base import CoreEntity

        if not issubclass(cls, CoreEntity):
            raise InvalidEntityTypeError('Input parameter [{cls}] is '
                                         'not a subclass of CoreEntity.'
                                         .format(cls=str(cls)))

        # registering model into database binds.
        self._binds[cls] = bind_name

    def _map_entity_to_engine(self):
        """
        maps all application entities to relevant engines.

        :raises InvalidDatabaseBindError: invalid database bind error.
        """

        binds = config_services.get_active_section('database.binds')

        for entity, bind_name in self._binds.items():
            if bind_name not in binds:
                raise InvalidDatabaseBindError('Database bind name [{bind_name}] for entity '
                                               '[{entity_name}] is not available in '
                                               'database.binds.config file.'
                                               .format(bind_name=bind_name,
                                                       entity_name=str(entity)))

            self._entity_to_engine_map[entity] = self.__bounded_engines[bind_name]

    def configure_session_factories(self):
        """
        configures all application session factories.
        normally, you should not call this method manually.

        :raises InvalidDatabaseBindError: invalid database bind error.
        """

        self._map_entity_to_engine()

        if len(self._entity_to_engine_map) > 0:
            for key in self._session_factories.keys():
                self._session_factories[key].configure(binds=self._entity_to_engine_map)
