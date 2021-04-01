# -*- coding: utf-8 -*-
"""
database services module.
"""

from pyrin.application.services import get_component
from pyrin.database import DatabasePackage


def get_current_store(**kwargs):
    """
    gets current database store.

    note that this method will always get the correct session based on available
    context. so if you are in an atomic context, it gets you the correct atomic
    session, but if you are not in an atomic context, it will get you the related
    session to current scope.

    :keyword object **kwargs: keyword arguments will be passed to the
                              `CoreScopedSession.session_factory` callable
                              to configure the new session that's being
                              created, if an existing session is not present.
                              if the session is present and keyword arguments
                              have been passed, an error will be raised.

    :raises ScopedSessionIsAlreadyPresentError: scoped session is already present error.

    :returns: database session
    :rtype: CoreSession
    """

    return get_component(DatabasePackage.COMPONENT_NAME).get_current_store(**kwargs)


def get_current_session_factory():
    """
    gets current database session factory.

    this method should not be used directly for data manipulation.
    use `get_current_store` method instead.

    :returns: database session factory
    :rtype: CoreScopedSession
    """

    return get_component(DatabasePackage.COMPONENT_NAME).get_current_session_factory()


def get_atomic_store(**kwargs):
    """
    gets an atomic database store.

    atomic is meaning a new session with a new transaction. note that it's normally
    not needed to get an atomic session manually, instead you could use `@atomic`
    decorator to provide you an atomic session. but if you really need to get an atomic
    session manually, you have to manually remove that session from corresponding
    session factory after you've done. otherwise, unexpected behaviour may occur.
    so if you get an atomic session, and don't remove it, after that if you get another
    session in the same scope, you will get the same exact atomic session. but if you
    get an atomic session, and remove it from corresponding session factory after you've
    done, after that if you get a session, it will get you a session related to current
    scope. this is why it's recommended not to get an atomic session manually, and
    instead use `@atomic` decorator when you need an atomic session.

    :keyword bool expire_on_commit: expire atomic session after commit.
                                    it is useful to set it to True if
                                    the atomic function does not return
                                    any entities for post-processing.
                                    defaults to False if not provided.

    :keyword object **kwargs: keyword arguments will be passed to the
                              `CoreScopedSession.session_factory` callable
                              to configure the new atomic session that's
                              being created.

    :returns: database session
    :rtype: CoreSession
    """

    return get_component(DatabasePackage.COMPONENT_NAME).get_atomic_store(**kwargs)


def finalize_transaction(response, **options):
    """
    this method will finalize database transaction of each request.

    this method will finalize both normal and atomic sessions of
    current request if available.
    we should not raise any exception in finalize transaction hook,
    so we return an error response in case of any exception.
    note that normally you should never call this method manually.

    :param CoreResponse response: response object.

    :rtype: CoreResponse | tuple
    """

    return get_component(DatabasePackage.COMPONENT_NAME).finalize_transaction(response,
                                                                              **options)


def cleanup_session(exception):
    """
    this method will cleanup database session of each request.

    this method will cleanup both normal and atomic sessions of
    current request if available.
    in case of any unhandled exception. we should not raise any exception
    in teardown request handlers, so we just log the exception.
    note that normally you should never call this method manually.

    :param Exception exception: exception instance.
    """

    return get_component(DatabasePackage.COMPONENT_NAME).cleanup_session(exception)


def register_session_factory(instance, **options):
    """
    registers a new session factory or replaces the existing one.

    if `replace=True` is provided. otherwise, it raises an error
    on adding an instance which it's `request_bounded` is already available
    in registered session factories.

    :param AbstractSessionFactoryBase instance: session factory to be registered.
                                                it must be an instance of
                                                AbstractSessionFactoryBase.

    :keyword bool replace: specifies that if there is another registered
                           session factory with the same `request_bounded`,
                           replace it with the new one, otherwise raise an error.
                           defaults to False.

    :raises InvalidSessionFactoryTypeError: invalid session factory type error.
    :raises DuplicatedSessionFactoryError: duplicated session factory error.
    """

    return get_component(DatabasePackage.COMPONENT_NAME).register_session_factory(instance,
                                                                                  **options)


def register_bind(entity, bind_name, **options):
    """
    binds the given model class with specified bind database.

    :param type[BaseEntity] entity: base entity subclass to be bounded.
    :param str bind_name: bind name to be associated with the model class.

    :raises InvalidEntityTypeError: invalid entity type error.
    """

    return get_component(DatabasePackage.COMPONENT_NAME).register_bind(entity, bind_name,
                                                                       **options)


def configure_session_factories():
    """
    configures all application session factories.

    normally, you should not call this method manually.

    :raises InvalidDatabaseBindError: invalid database bind error.
    """

    return get_component(DatabasePackage.COMPONENT_NAME).configure_session_factories()


def get_default_engine():
    """
    gets database default engine.

    :rtype: Engine
    """

    return get_component(DatabasePackage.COMPONENT_NAME).get_default_engine()


def get_bounded_engines():
    """
    gets database bounded engines.

    :returns: dict[str bind_name: Engine engine]
    :rtype: dict
    """

    return get_component(DatabasePackage.COMPONENT_NAME).get_bounded_engines()


def get_entity_to_engine_map():
    """
    gets entity to engine map.

    :returns: dict[type entity, Engine engine]
    :rtype: dict
    """

    return get_component(DatabasePackage.COMPONENT_NAME).get_entity_to_engine_map()


def get_table_name_to_engine_map():
    """
    gets table name to engine map.

    :returns: dict[str table_name, Engine engine]
    :rtype: dict
    """

    return get_component(DatabasePackage.COMPONENT_NAME).get_table_name_to_engine_map()


def register_hook(instance):
    """
    registers the given instance into database hooks.

    :param DatabaseHookBase instance: database hook instance to be registered.

    :raises InvalidDatabaseHookTypeError: invalid database hook type error.
    """

    return get_component(DatabasePackage.COMPONENT_NAME).register_hook(instance)


def get_table_engine(table_name):
    """
    gets the database engine which the provided table name is bounded to.

    :param str table_name: table name to get its bounded engine.

    :rtype: Engine
    """

    return get_component(DatabasePackage.COMPONENT_NAME).get_table_engine(table_name)


def get_bind_name_engine(bind_name):
    """
    gets the database engine which the provided bind name is bounded to.

    :param str bind_name: bind name to get its bounded engine.

    :raises InvalidDatabaseBindError: invalid database bind error.

    :rtype: Engine
    """

    return get_component(DatabasePackage.COMPONENT_NAME).get_bind_name_engine(bind_name)


def get_entity_engine(entity):
    """
    gets the database engine which the provided entity class is bounded to.

    :param BaseEntity entity: entity class to get its bounded engine.

    :rtype: Engine
    """

    return get_component(DatabasePackage.COMPONENT_NAME).get_entity_engine(entity)


def get_bind_config_section_name(bind_name):
    """
    gets the bind config section name for given bind name and currently
    active environment in 'database.ini' from 'database.binds.ini' file.

    :param str bind_name: bind name to get its section name.

    :rtype: str
    """

    return get_component(DatabasePackage.COMPONENT_NAME).get_bind_config_section_name(bind_name)


def get_default_database_name():
    """
    gets default database name.

    :rtype: str
    """

    return get_component(DatabasePackage.COMPONENT_NAME).get_default_database_name()


def get_configs_prefix():
    """
    gets the configs prefix for sqlalchemy keys in database config store.

    it gets the value of `configs_prefix` key from database config store.

    :rtype: str
    """

    return get_component(DatabasePackage.COMPONENT_NAME).get_configs_prefix()


def get_all_database_names():
    """
    gets all database names defined in application.

    it returns all available database names, even those
    that do not have any entity bounded to them.
    the result also includes the default database name.

    :rtype: list[str]
    """

    return get_component(DatabasePackage.COMPONENT_NAME).get_all_database_names()


def get_database_bind_names():
    """
    gets all database bind names defined in application.

    it returns all available database bind names, even those
    that do not have any entity bounded to them.

    :rtype: list[str]
    """

    return get_component(DatabasePackage.COMPONENT_NAME).get_database_bind_names()
