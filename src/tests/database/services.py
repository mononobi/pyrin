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


def get_session_factory():
    """
    gets database session factory.
    this method should not be used directly for data manipulation.
    use `get_current_store` method instead.

    :returns: database session factory
    :rtype: Session
    """

    return get_component(DatabasePackage.COMPONENT_NAME).get_session_factory()


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
