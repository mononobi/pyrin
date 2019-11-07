# -*- coding: utf-8 -*-
"""
database test_services module.
"""

import pytest

import pyrin.database.services as database_services

from pyrin.core.context import CoreObject
from pyrin.database.exceptions import DuplicatedSessionFactoryError, InvalidSessionFactoryTypeError
from pyrin.database.session_factory.request_scoped import RequestScopedSessionFactory
from pyrin.database.session_factory.thread_scoped import ThreadScopedSessionFactory


def test_get_current_store_unbounded():
    """
    gets current database store which should be of request unbounded type.
    """

    store = database_services.get_current_store()
    assert store is not None
    assert store.autocommit is False


def test_get_session_factory_current():
    """
    gets the correct current database session factory.
    it should be of request unbounded type.
    """

    session_factory = database_services.get_session_factory()
    assert session_factory.is_request_bounded is False
    assert session_factory.session_factory_name == 'ThreadScopedSessionFactory'


def test_get_session_factory_unbounded():
    """
    gets the request unbounded database session factory.
    """

    session_factory = database_services.get_session_factory(request_bounded=False)
    assert session_factory.is_request_bounded is False
    assert session_factory.session_factory_name == 'ThreadScopedSessionFactory'


def test_get_session_factory_bounded():
    """
    gets the request bounded database session factory.
    """

    session_factory = database_services.get_session_factory(request_bounded=True)
    assert session_factory.is_request_bounded is True
    assert session_factory.session_factory_name == 'RequestScopedSessionFactory'


def test_register_session_factory_invalid_type():
    """
    registers a session factory which has an invalid type.
    it should raise an error.
    """

    with pytest.raises(InvalidSessionFactoryTypeError):
        instance = CoreObject()
        database_services.register_session_factory(instance)


def test_register_session_factory_duplicate_bounded():
    """
    registers a duplicated session factory of request bounded type.
    it should raise an error.
    """

    with pytest.raises(DuplicatedSessionFactoryError):
        instance = RequestScopedSessionFactory()
        database_services.register_session_factory(instance)


def test_register_session_factory_duplicate_unbounded():
    """
    registers a duplicated session factory of request unbounded type.
    it should raise an error.
    """

    with pytest.raises(DuplicatedSessionFactoryError):
        instance = ThreadScopedSessionFactory()
        database_services.register_session_factory(instance)


def test_register_session_factory_duplicate_with_replace():
    """
    registers a duplicated session factory with replace option.
    it should not raise an error.
    """

    instance = RequestScopedSessionFactory()
    database_services.register_session_factory(instance, replace=True)
