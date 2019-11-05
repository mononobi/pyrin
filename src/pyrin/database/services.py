# -*- coding: utf-8 -*-
"""
database services module.
"""

from pyrin.application.decorators import after_request_handler, teardown_request_handler
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


@after_request_handler()
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


@teardown_request_handler()
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

    :param SessionFactoryBase instance: session factory to be registered.
                                        it must be an instance of SessionFactoryBase.

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
