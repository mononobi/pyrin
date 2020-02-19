# -*- coding: utf-8 -*-
"""
database manager module.
"""

from sqlalchemy import engine_from_config

import pyrin.configuration.services as config_services
import pyrin.logging.services as logging_services
import pyrin.security.session.services as session_services
import pyrin.utils.dictionary as dict_utils

from pyrin.core.globals import LIST_TYPES
from pyrin.database.hooks import DatabaseHookBase
from pyrin.core.mixin import HookMixin
from pyrin.database.model.base import CoreEntity
from pyrin.core.context import DTO, Manager
from pyrin.core.enumerations import ClientErrorResponseCodeEnum, ServerErrorResponseCodeEnum
from pyrin.database.interface import AbstractSessionFactoryBase
from pyrin.utils import response as response_utils
from pyrin.utils.custom_print import print_warning
from pyrin.database.exceptions import InvalidSessionFactoryTypeError, \
    DuplicatedSessionFactoryError, SessionFactoryNotExistedError, InvalidEntityTypeError, \
    InvalidDatabaseBindError


class DatabaseManager(Manager, HookMixin):
    """
    database manager class.
    """

    LOGGER = logging_services.get_logger('database')
    BIND_REMOVE_KEY_PREFIX = '__'
    DEFAULT_DATABASE_NAME = 'default'
    _hook_type = DatabaseHookBase

    def __init__(self):
        """
        initializes an instance of DatabaseManager.
        """

        super().__init__()

        # contains the application default database engine.
        self.___engine = self._create_default_engine()

        # a dictionary containing engines for different bounded databases.
        # in the form of: {str bind_name: Engine engine}
        self.__bounded_engines = self._create_bounded_engines()

        # a dictionary containing all entity classes that should be
        # bounded into a database engine other than the default one.
        # in the form of: {type entity: str bind_name}
        self._binds = DTO()

        # a dictionary containing entity to engine map for those entities that
        # should be bounded to a different database engine than the default one.
        # in the form of: {type entity: Engine engine}
        self._entity_to_engine_map = DTO()

        # a dictionary containing table name to engine map for those entities that
        # should be bounded to a different database engine than the default one.
        # in the form of: {string table_name: Engine engine}
        self._table_name_to_engine_map = DTO()

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

        configs_prefix = config_services.get_active('database', 'configs_prefix')
        return engine_from_config(database_configs, prefix=configs_prefix, **kwargs)

    def _create_bounded_engines(self):
        """
        creates all required bounded engines if any and returns them.

        :returns: dict(str bind_name: Engine engine)
        :rtype: dict
        """

        engines = DTO()
        base_database_configs = config_services.get_active_section('database')
        binds_names = base_database_configs['bind_names']

        if binds_names is None:
            return engines
        if not isinstance(binds_names, LIST_TYPES):
            binds_names = [binds_names]
        if len(binds_names) <= 0:
            return engines

        for name in binds_names:
            bind_configs = self._get_bind_configs(name)
            full_configs = self._merge_configs(base_database_configs, bind_configs)
            engine = self._create_engine(full_configs)
            engines[name] = engine

        return engines

    def _merge_configs(self, base_configs, bind_configs):
        """
        merges given base and bind configs and returns a new dict.
        merging will cause all keys in bind configs override any available key in
        base configs. also all keys that are present in bind configs and starting
        with double underscore `__` will be removed from result dict and also all
        keys that their names are exactly like prefixed ones but without `__` will
        be removed from result dict.

        :param dict base_configs: base configs from `database.config` file.
        :param dict bind_configs: bind configs from `database.binds.config`

        :rtype: dict
        """

        result = DTO(**base_configs)
        result.update(**bind_configs)
        result = dict_utils.remove_keys(result, self.BIND_REMOVE_KEY_PREFIX)

        return result

    def _get_bind_configs(self, bind_name):
        """
        gets all bind configs of given bind name for currently
        active environment in 'database.config' from 'database.binds.config' file.

        :param str bind_name: bind name to get its configs.

        :rtype: dict
        """

        bind_configs_section = self.get_bind_config_section_name(bind_name)
        return config_services.get_section('database.binds', bind_configs_section)

    def get_bind_config_section_name(self, bind_name):
        """
        gets the bind config section name for given bind name and currently
        active environment in 'database.config' from 'database.binds.config' file.

        :param str bind_name: bind name to get its section name.

        :rtype: str
        """

        active_environment = config_services.get_active_section_name('database')
        bind_config_key = '{environment}_{bind_name}'.format(environment=active_environment,
                                                             bind_name=bind_name)

        return bind_config_key

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
            store = self.get_current_store()
            session_factory = self.get_session_factory()
            try:
                if response.status_code >= ClientErrorResponseCodeEnum.BAD_REQUEST:
                    store.rollback()
                    return response

                store.commit()
                return response
            except Exception:
                store.rollback()
                raise
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
                self.LOGGER.exception(str(exception))
                session_factory = self.get_session_factory()
                session_factory.remove()

            except Exception as error:
                self.LOGGER.exception(str(error))

    def register_session_factory(self, instance, **options):
        """
        registers a new session factory or replaces the existing one
        if `replace=True` is provided. otherwise, it raises an error
        on adding an instance which it's is_request_bounded() is already available
        in registered session factories.

        :param AbstractSessionFactoryBase instance: session factory to be registered.
                                                    it must be an instance of
                                                    AbstractSessionFactoryBase.

        :keyword bool replace: specifies that if there is another registered
                               session factory with the same is_request_bounded(),
                               replace it with the new one, otherwise raise an error.
                               defaults to False.

        :raises InvalidSessionFactoryTypeError: invalid session factory type error.
        :raises DuplicatedSessionFactoryError: duplicated session factory error.
        """

        if not isinstance(instance, AbstractSessionFactoryBase):
            raise InvalidSessionFactoryTypeError('Input parameter [{instance}] is '
                                                 'not an instance of [{base}].'
                                                 .format(instance=str(instance),
                                                         base=AbstractSessionFactoryBase))

        # checking whether is there any registered
        # instance with the same 'is_request_bounded()' value.
        if instance.is_request_bounded() in self._session_factories:
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
            instance.create_session_factory(self.get_default_engine())

    def register_bind(self, entity, bind_name, **options):
        """
        binds the given model class with specified bind database.

        :param CoreEntity entity: CoreEntity subclass to be bounded.
        :param str bind_name: bind name to be associated with the model class.

        :raises InvalidEntityTypeError: invalid entity type error.
        """

        if not issubclass(entity, CoreEntity):
            raise InvalidEntityTypeError('Input parameter [{entity}] is '
                                         'not a subclass of [{base}].'
                                         .format(entity=entity,
                                                 base=CoreEntity))

        # registering model into database binds.
        self._binds[entity] = bind_name

    def _map_entity_to_engine(self):
        """
        maps all application entities that should be bounded to a
        database engine other than the default one to relevant engines.

        :raises InvalidDatabaseBindError: invalid database bind error.
        """

        binds = config_services.get_active('database', 'bind_names')
        if binds is None:
            binds = []
        if not isinstance(binds, LIST_TYPES):
            binds = [binds]

        for entity, bind_name in self._binds.items():
            if bind_name not in binds:
                raise InvalidDatabaseBindError('Database bind name [{bind_name}] for entity '
                                               '[{entity_name}] is not available in '
                                               'database config store.'
                                               .format(bind_name=bind_name,
                                                       entity_name=entity))

            self._entity_to_engine_map[entity] = self.get_bounded_engines()[bind_name]
            self._table_name_to_engine_map[entity.table_name().lower()] = \
                self.get_bounded_engines()[bind_name]
            self._table_name_to_engine_map[entity.table_fullname().lower()] = \
                self.get_bounded_engines()[bind_name]

    def configure_session_factories(self):
        """
        configures all application session factories.
        normally, you should not call this method manually.

        :raises InvalidDatabaseBindError: invalid database bind error.
        """

        self._map_entity_to_engine()

        if len(self.get_entity_to_engine_map()) > 0:
            for key in self._session_factories:
                self._session_factories[key].configure(binds=self.get_entity_to_engine_map())

        self._after_session_factories_configured()

    def get_default_engine(self):
        """
        gets database default engine.

        :rtype: Engine
        """

        return self.___engine

    def get_bounded_engines(self):
        """
        gets database bounded engines.

        :returns: dict(str bind_name: Engine engine)
        :rtype: dict
        """

        return self.__bounded_engines

    def get_entity_to_engine_map(self):
        """
        gets entity to engine map.

        :returns: dict(type entity, Engine engine)
        :rtype: dict
        """

        return self._entity_to_engine_map

    def get_table_name_to_engine_map(self):
        """
        gets table name to engine map.

        :returns: dict(str table_name, Engine engine)
        :rtype: dict
        """

        return self._table_name_to_engine_map

    def _after_session_factories_configured(self):
        """
        this method will call `after_session_factories_configured`
        method of all registered hooks.
        """

        for hook in self._get_hooks():
            hook.after_session_factories_configured()

    def get_entity_engine(self, entity):
        """
        gets the database engine which the provided entity class is bounded to.

        :param CoreEntity entity: entity class to get its bounded engine.

        :rtype: Engine
        """

        if entity in self.get_entity_to_engine_map():
            return self.get_entity_to_engine_map()[entity]

        return self.get_default_engine()

    def get_table_engine(self, table_name):
        """
        gets the database engine which the provided table name is bounded to.

        :param str table_name: table name to get its bounded engine.

        :rtype: Engine
        """

        table_name = table_name.lower()
        if table_name in self.get_table_name_to_engine_map():
            return self.get_table_name_to_engine_map()[table_name]

        return self.get_default_engine()

    def get_bind_name_engine(self, bind_name):
        """
        gets the database engine which the provided bind name is bounded to.

        :param str bind_name: bind name to get its bounded engine.

        :raises InvalidDatabaseBindError: invalid database bind error.

        :rtype: Engine
        """

        if bind_name == self.DEFAULT_DATABASE_NAME:
            return self.get_default_engine()

        elif bind_name in self.get_bounded_engines():
            return self.get_bounded_engines()[bind_name]

        raise InvalidDatabaseBindError('Database bind name [{bind_name}] does '
                                       'not exist in database config store.'
                                       .format(bind_name=bind_name))

    def get_default_database_name(self):
        """
        gets default database name.

        :rtype: str
        """

        return self.DEFAULT_DATABASE_NAME
