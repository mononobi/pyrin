# -*- coding: utf-8 -*-
"""
database test_services module.
"""

import pytest

import pyrin.database.services as database_services
import pyrin.configuration.services as config_services

from pyrin.core.context import CoreObject
from pyrin.database.session_factory.request_scoped import RequestScopedSessionFactory
from pyrin.database.session_factory.thread_scoped import ThreadScopedSessionFactory
from pyrin.database.exceptions import DuplicatedSessionFactoryError, \
    InvalidSessionFactoryTypeError, InvalidEntityTypeError, InvalidDatabaseBindError

import tests.database.services as extended_database_services

from tests.common.models import BoundedLocalEntity, BoundedTestEntity, SampleTestEntity, \
    ManualBoundedLocalEntity


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


def test_register_bind():
    """
    registers a model into binds list.
    """

    database_services.register_bind(ManualBoundedLocalEntity, 'local')
    binds = extended_database_services.get_binds()
    assert len(binds) >= 2
    assert ManualBoundedLocalEntity in binds
    assert binds[ManualBoundedLocalEntity] == 'local'
    database_services.configure_session_factories()


def test_register_bind_invalid_type():
    """
    registers an object which has invalid type into binds list.
    it should raise an error.
    """

    with pytest.raises(InvalidEntityTypeError):
        database_services.register_bind(CoreObject, 'local')


def test_configure_session_factories_invalid_bind():
    """
    configures all application session factories.
    there is an entity which is bounded to an invalid bind name.
    it should raise an error.
    """

    database_services.register_bind(SampleTestEntity, 'invalid_bind_name')

    try:
        with pytest.raises(InvalidDatabaseBindError):
            database_services.configure_session_factories()
    finally:
        extended_database_services.remove_bind(SampleTestEntity)


def test_get_binds():
    """
    gets all bounded entities.
    """

    binds = extended_database_services.get_binds()

    assert len(binds) >= 2
    assert BoundedLocalEntity in binds
    assert binds[BoundedLocalEntity] == 'local'
    assert BoundedTestEntity in binds
    assert binds[BoundedTestEntity] == 'test'


def test_get_entity_to_engine_map():
    """
    gets entity to engine map dictionary.
    """

    entity_to_engine_map = extended_database_services.get_entity_to_engine_map()
    active_section = config_services.get_active_section('database.binds')

    assert entity_to_engine_map is not None
    assert len(entity_to_engine_map) >= 2
    assert BoundedLocalEntity in entity_to_engine_map
    assert BoundedTestEntity in entity_to_engine_map

    local_engine = entity_to_engine_map[BoundedLocalEntity]
    test_engine = entity_to_engine_map[BoundedTestEntity]

    assert local_engine is not None
    assert test_engine is not None
    assert str(local_engine.url) == active_section['local']
    assert str(test_engine.url) == active_section['test']


def test_get_engine_to_table_map():
    """
    gets engine to table map dictionary.
    """

    engine_to_table_map = extended_database_services.get_engine_to_table_map()
    all_engines = extended_database_services.get_all_engines()

    assert engine_to_table_map is not None
    assert len(engine_to_table_map) >= 3
    assert all(engine in engine_to_table_map for engine in all_engines)


def test_create_all():
    """
    creates all entities on database engine.
    """

    database_services.create_all()


def test_drop_all():
    """
    drops all entities on database engine.
    """

    database_services.drop_all()
