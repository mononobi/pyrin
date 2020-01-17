# -*- coding: utf-8 -*-
"""
application test_services module.
"""

import os

import pytest

import pyrin.application.services as application_services
import pyrin.utils.path as path_utils

from pyrin.settings.static import DEFAULT_COMPONENT_KEY
from pyrin.application.context import Component
from pyrin.core.context import CoreObject, DTO
from pyrin.core.enumerations import HTTPMethodEnum
from pyrin.application.exceptions import DuplicateContextKeyError, DuplicateComponentIDError, \
    DuplicateRouteURLError, InvalidRouteFactoryTypeError, InvalidComponentTypeError, \
    InvalidComponentNameError, ComponentAttributeError

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


def test_register_component_with_custom_key():
    """
    registers given application component with custom key.
    """

    default_component = Component('default_component')
    custom_component = Component('default_component', component_custom_key=1000)
    application_services.register_component(default_component)
    application_services.register_component(custom_component)
    assert application_services.get_component('default_component') == default_component
    assert application_services.get_component('default_component',
                                              component_custom_key=1000) == custom_component


def test_register_component_with_custom_key_duplicate():
    """
    registers given application component with duplicated custom key.
    it should raise an error.
    """

    with pytest.raises(DuplicateComponentIDError):
        default_component = Component('default_component_duplicate')
        custom_component1 = Component('default_component_duplicate', component_custom_key=1000)
        custom_component2 = Component('default_component_duplicate', component_custom_key=1000)
        application_services.register_component(default_component)
        application_services.register_component(custom_component1)
        application_services.register_component(custom_component2)


def test_register_component_with_custom_key_duplicate_with_replace():
    """
    registers given application component with duplicated custom key and replace option.
    it should not raise an error.
    """

    default_component = Component('default_component_duplicate_replace')
    custom_component1 = Component('default_component_duplicate_replace',
                                  component_custom_key=2000)
    custom_component2 = Component('default_component_duplicate_replace',
                                  component_custom_key=2000)
    application_services.register_component(default_component)
    application_services.register_component(custom_component1)
    application_services.register_component(custom_component2, replace=True)
    assert application_services.get_component('default_component_duplicate_replace') \
        == default_component

    assert application_services.get_component('default_component_duplicate_replace',
                                              component_custom_key=2000) \
        == custom_component2


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
    registers given duplicate application component with
    replace option and should not raise an error.
    """

    component = Component('component_duplicate2')
    component_duplicate = Component('component_duplicate2')
    application_services.register_component(component)
    application_services.register_component(component_duplicate, replace=True)
    assert application_services.get_component('component_duplicate2') == component_duplicate


def test_register_component_duplicate_with_replace_with_custom_attributes():
    """
    registers given duplicate application component which has some list and
    dict attributes and attributes with three consecutive underlines in their
    names that should be passed to new component with replace option.
    """

    component = Component('component_duplicate_with_custom_attrs')
    component_duplicate = Component('component_duplicate_with_custom_attrs')

    setattr(component, '__private_field', True)
    setattr(component, '_protected_field', 21)
    setattr(component, 'public_field', 'public')
    setattr(component, 'list_field', [1, 2, 3])
    setattr(component, 'dict_field', dict(name='a', age=23))
    setattr(component, '___old_attribute', 'old')

    setattr(component_duplicate, 'child_attribute', 100)
    setattr(component_duplicate, '__private_field', False)
    setattr(component_duplicate, '_protected_field', 450)
    setattr(component_duplicate, 'list_field', [10, 20, 30])
    setattr(component_duplicate, 'dict_field', dict(car='BMW', price=10000))
    setattr(component_duplicate, '___old_attribute', 'new')

    application_services.register_component(component)
    application_services.register_component(component_duplicate, replace=True)

    newly_added_component = application_services.get_component(
        'component_duplicate_with_custom_attrs')

    assert newly_added_component is not None
    assert hasattr(newly_added_component, '__private_field') is True
    assert hasattr(newly_added_component, '_protected_field') is True
    assert hasattr(newly_added_component, 'public_field') is False
    assert hasattr(newly_added_component, 'child_attribute') is True
    assert hasattr(newly_added_component, 'list_field') is True
    assert hasattr(newly_added_component, 'dict_field') is True
    assert hasattr(newly_added_component, '___old_attribute') is True

    assert getattr(newly_added_component, '__private_field') is False
    assert getattr(newly_added_component, '_protected_field') == 450
    assert getattr(newly_added_component, 'child_attribute') == 100
    assert getattr(newly_added_component, 'list_field') == [1, 2, 3]
    assert getattr(newly_added_component, 'dict_field') == dict(name='a', age=23)
    assert getattr(newly_added_component, '___old_attribute') == 'old'


def test_get_component_with_invalid_name():
    """
    gets the application component with given name which is unavailable.
    it should raise an error.
    """

    with pytest.raises(ComponentAttributeError):
        application_services.get_component('missing_component')


def test_get_component_with_invalid_custom_key():
    """
    gets the application component with given custom key which is unavailable.
    it should not raise an error and must get the default component.
    """

    component = Component('component_with_invalid_key')
    custom_component = Component('component_with_invalid_key', component_custom_key=3000)
    application_services.register_component(component)
    application_services.register_component(custom_component)
    assert application_services.get_component('component_with_invalid_key',
                                              component_custom_key=999) == component


def test_get_component_with_default_key():
    """
    gets the application component with default key.
    """

    component = Component('component_with_default_key')
    application_services.register_component(component)
    assert application_services.get_component('component_with_default_key',
                                              component_custom_key=DEFAULT_COMPONENT_KEY) \
        == component


def test_get_all_components():
    """
    gets all application components and asserts that all required components are available.
    """

    components = ['api.component',
                  'api.router.component',
                  'configuration.component',
                  'database.component',
                  'globalization.locale.component',
                  'globalization.datetime.component',
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

    assert all(application_services.get_component(component) is not None
               for component in components)


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

    configs = DTO()
    configs.update(fake_name='fake_name', fake_id='fake_id',
                   fake_number=33, fake_value='fake_value')
    application_services.configure(configs)

    app_configs = application_services.get_configs()
    assert all(name in app_configs for name in
               ['FAKE_NAME', 'FAKE_ID', 'FAKE_NUMBER', 'FAKE_VALUE'])

    assert not any(name in app_configs for name in
                   ['fake_name', 'fake_id', 'fake_number', 'fake_value'])


def test_all_configs_available():
    """
    checks that all application related configs are loaded from settings files.
    """

    app_configs = application_services.get_configs()
    assert all(name in app_configs for name in ['TITLE', 'BASE_CURRENCY', 'ENCODING',
                                                'FLASK_LOG_LEVEL', 'SERVER_NAME', 'SERVER_IP',
                                                'SERVER_PORT', 'SERVER_PROTOCOL', 'ENV',
                                                'DEBUG', 'TESTING', 'UNIT_TESTING'])


def test_all_configs_values():
    """
    checks that all application related configs are loaded with correct values.
    """

    app_configs = application_services.get_configs()

    assert app_configs['TITLE'] == 'pyrin_tests'
    assert app_configs['BASE_CURRENCY'] == 'IRR'
    assert app_configs['ENCODING'] == 'utf-8'
    assert app_configs['FLASK_LOG_LEVEL'] == 'DEBUG'
    assert app_configs['SERVER_NAME'] == 'pyrin.server:9083'
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
