# -*- coding: utf-8 -*-
"""
application test_services module.
"""

import os

import pytest

import pyrin.application.services as application_services
import pyrin.utils.path as path_utils

from pyrin.application.context import Component
from pyrin.core.context import CoreObject
from pyrin.core.enumerations import HTTPMethodEnum
from pyrin.application.exceptions import DuplicateContextKeyError, DuplicateComponentIDError, \
    DuplicateRouteURLError, InvalidRouteFactoryTypeError, InvalidComponentTypeError, \
    InvalidComponentNameError

from tests import PyrinTestApplication
from tests.common.mock_functions import mock_view_function, mock_route_factory


def test_add_context():
    """
    adds the given key and it's value into the application context.
    """

    application_services.add_context('context1', 'value1')
    assert application_services.get_context('context1') == 'value1'


def test_add_context_duplicate():
    """
    adds the given duplicate key and it's value into the
    application context and should raise an error.
    """

    with pytest.raises(DuplicateContextKeyError):
        application_services.add_context('context2', 'value2')
        application_services.add_context('context2', 'value4')


def test_add_context_duplicate_with_replace():
    """
    adds the given duplicate key and it's value into the
    application context with replace option and should not raise an error.
    """

    application_services.add_context('context3', 'value3')
    application_services.add_context('context3', 'value4', replace=True)
    assert application_services.get_context('context3') == 'value4'


def test_get_context():
    """
    gets the application context value that belongs to given key.
    """

    application_services.add_context('context4', 'value4')
    assert application_services.get_context('context4') == 'value4'


def test_register_component():
    """
    registers given application component.
    """

    component = Component('component1')
    application_services.register_component(component)
    assert application_services.get_component('component1') == component


def test_register_component_with_invalid_type():
    """
    registers given application component with invalid type.
    it should raise an error.
    """

    with pytest.raises(InvalidComponentTypeError):
        component = CoreObject()
        application_services.register_component(component)


def test_register_component_with_invalid_name():
    """
    registers given application component with invalid name.
    it should raise an error.
    """

    with pytest.raises(InvalidComponentNameError):
        component = Component('')
        application_services.register_component(component)


def test_register_component_duplicate():
    """
    registers given duplicate application component and should raise an error.
    """

    with pytest.raises(DuplicateComponentIDError):
        component = Component('component_duplicate')
        component_duplicate = Component('component_duplicate')
        application_services.register_component(component)
        application_services.register_component(component_duplicate)


def test_register_component_duplicate_with_replace():
    """
    registers given duplicate application component and
    with replace option and should not raise an error.
    """

    component = Component('component_duplicate2')
    component_duplicate = Component('component_duplicate2')
    application_services.register_component(component)
    application_services.register_component(component_duplicate, replace=True)
    assert application_services.get_component('component_duplicate2') == component_duplicate


def test_get_all_components():
    """
    gets all application components and asserts that all required components are available.
    """

    components = ['api.component',
                  'api.router.component',
                  'configuration.component',
                  'database.component',
                  'localization.component',
                  'logging.component',
                  'converters.deserializer.component',
                  'security.component',
                  'security.authentication.component',
                  'security.authorization.component',
                  'security.encryption.component',
                  'security.hashing.component',
                  'security.permission.component',
                  'security.session.component',
                  'security.token.component']

    for component in components:
        assert application_services.get_component(component) is not None


def test_add_url_rule():
    """
    adds a url rule into application rules.
    """

    application_services.add_url_rule('/tests/application/rule', view_func=mock_view_function,
                                      methods=HTTPMethodEnum.GET)


def test_add_url_rule_duplicate():
    """
    adds a duplicate url rule into application rules and should raise an error.
    """

    with pytest.raises(DuplicateRouteURLError):
        application_services.add_url_rule('/tests/application/duplicate/rule',
                                          view_func=mock_view_function,
                                          methods=HTTPMethodEnum.GET)

        application_services.add_url_rule('/tests/application/duplicate/rule',
                                          view_func=mock_view_function,
                                          methods=HTTPMethodEnum.GET)


def test_add_url_rule_duplicate_with_replace():
    """
    adds a duplicate url rule into application rules with
    replace option and should not raise an error.
    """

    application_services.add_url_rule('/tests/application/duplicate/rule2',
                                      view_func=mock_view_function,
                                      methods=HTTPMethodEnum.POST)

    application_services.add_url_rule('/tests/application/duplicate/rule2',
                                      view_func=mock_view_function,
                                      methods=HTTPMethodEnum.GET,
                                      replace=True)


def test_register_route_factory():
    """
    registers a route factory as application url rule class.
    """

    current_factory = application_services.get_current_route_factory()
    application_services.register_route_factory(mock_route_factory)
    assert application_services.get_current_route_factory() == mock_route_factory
    application_services.register_route_factory(current_factory)


def test_register_route_factory_not_callable():
    """
    registers a not callable route factory as application
    url rule class. it should raise an error.
    """

    with pytest.raises(InvalidRouteFactoryTypeError):
        application_services.register_route_factory(1)


def test_get_settings_path():
    """
    gets the application settings path.
    """

    root_path = path_utils.resolve_application_root_path()
    settings_path = os.path.join(root_path, 'tests/settings')
    assert application_services.get_settings_path() == settings_path


def test_configure():
    """
    configures the application with given dict.
    all keys will be converted to uppercase for flask compatibility.
    """

    configs = {}
    configs.update(fake_name='fake_name', fake_id='fake_id',
                   fake_number=33, fake_value='fake_value')
    application_services.configure(configs)

    app_configs = application_services.get_configs()
    assert all(name in app_configs for name in
               ['FAKE_NAME', 'FAKE_ID', 'FAKE_NUMBER', 'FAKE_VALUE']) is True

    assert all(name in app_configs for name in
               ['fake_name', 'fake_id', 'fake_number', 'fake_value']) is False


def test_all_configs_available():
    """
    checks that all application related configs are loaded from settings files.
    """

    app_configs = application_services.get_configs()
    assert all(name in app_configs for name in ['TITLE', 'BASE_CURRENCY', 'ENCODING',
                                                'FLASK_LOG_LEVEL', 'SERVER_NAME', 'SERVER_IP',
                                                'SERVER_PORT', 'SERVER_PROTOCOL', 'ENV',
                                                'DEBUG', 'TESTING', 'UNIT_TESTING']) is True


def test_all_configs_values():
    """
    checks that all application related configs are loaded with correct values.
    """

    app_configs = application_services.get_configs()

    assert app_configs['TITLE'] == 'pyrin_tests'
    assert app_configs['BASE_CURRENCY'] == 'IRR'
    assert app_configs['ENCODING'] == 'utf-8'
    assert app_configs['FLASK_LOG_LEVEL'] == 'DEBUG'
    assert app_configs['SERVER_NAME'] == 'localhost.localdomain:9083'
    assert app_configs['SERVER_IP'] == '127.0.0.1'
    assert app_configs['SERVER_PORT'] == 9083
    assert app_configs['SERVER_PROTOCOL'] == 'ssl'
    assert app_configs['ENV'] == 'testing'
    assert app_configs['DEBUG'] is False
    assert app_configs['TESTING'] is True
    assert app_configs['UNIT_TESTING'] is True


def test_get_current_app():
    """
    gets the instance of current running application.
    """

    assert isinstance(application_services.get_current_app(), PyrinTestApplication)
