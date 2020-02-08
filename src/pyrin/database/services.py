# -*- coding: utf-8 -*-
"""
database services module.
"""

from pyrin.application.services import get_component
from pyrin.database import DatabasePackage


def get_current_store():
    """
    gets current database store.

    :returns: database session
    :rtype: Session
    """

    return get_component(DatabasePackage.COMPONENT_NAME).get_current_store()


def get_session_factory(request_bounded=None):
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

    return get_component(DatabasePackage.COMPONENT_NAME).get_session_factory(request_bounded)


def finalize_transaction(response):
    """
    this method will finalize database transaction of each request.
    we should not raise any exception in request handlers, so we return
    an error response in case of any exception.
    note that normally you should never call this method manually.

    :param CoreResponse response: response object.

    :rtype: CoreResponse
    """

    return get_component(DatabasePackage.COMPONENT_NAME).finalize_transaction(response)


def cleanup_session(exception):
    """
    this method will cleanup database session of each request in
    case of any unhandled exception. we should not raise any exception
    in teardown request handlers, so we just log the exception.
    note that normally you should never call this method manually.

    :param Exception exception: exception instance.
    """

    return get_component(DatabasePackage.COMPONENT_NAME).cleanup_session(exception)


def register_session_factory(instance, **options):
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

    return get_component(DatabasePackage.COMPONENT_NAME).register_session_factory(instance,
                                                                                  **options)


def register_bind(cls, bind_name, **options):
    """
    binds the given model class with specified bind database.

    :param CoreEntity cls: CoreEntity subclass to be bounded.
    :param str bind_name: bind name to be associated with the model class.

    :raises InvalidEntityTypeError: invalid entity type error.
    """

    return get_component(DatabasePackage.COMPONENT_NAME).register_bind(cls, bind_name, **options)


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

    :returns: dict(str bind_name: Engine engine)
    :rtype: dict
    """

    return get_component(DatabasePackage.COMPONENT_NAME).get_bounded_engines()


def get_entity_to_engine_map():
    """
    gets entity to engine map.

    :returns: dict(type entity, Engine engine)
    :rtype: dict
    """

    return get_component(DatabasePackage.COMPONENT_NAME).get_entity_to_engine_map()


def get_table_name_to_engine_map():
    """
    gets table name to engine map.

    :returns: dict(str table_name, Engine engine)
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


def get_engine(entity_class):
    """
    gets the database engine which this entity is bounded to.

    :param CoreEntity entity_class: entity class to get its bounded engine.

    :rtype: Engine
    """

    return get_component(DatabasePackage.COMPONENT_NAME).get_engine(entity_class)
