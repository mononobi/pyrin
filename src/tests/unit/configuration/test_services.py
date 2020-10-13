# -*- coding: utf-8 -*-
"""
configuration test_services module.
"""

import os

from datetime import date

import pytest

from sqlalchemy.pool import Pool, StaticPool

import pyrin.application.services as application_services
import pyrin.configuration.services as config_services
import pyrin.utils.string as string_utils

from pyrin.configuration.exceptions import ConfigurationStoreExistedError, \
    ConfigurationFileNotFoundError, ConfigurationStoreNotFoundError, \
    ConfigurationStoreSectionNotFoundError, ConfigurationStoreKeyNotFoundError, \
    ConfigurationStoreDuplicateKeyError, ConfigurationFileExistedError

from tests.unit.common.utils import create_config_file, delete_config_file, \
    assert_config_file_not_existed, assert_config_file_existed


def test_load_configuration():
    """
    loads the configuration store from it's relevant file.
    the store has not been loaded yet.
    """

    try:
        create_config_file('new_settings_load.ini')
        config_services.load_configuration('new_settings_load')
        sections = config_services.get_section_names('new_settings_load')
        assert sections is not None
    finally:
        delete_config_file('new_settings_load.ini')


def test_load_configuration_already_loaded():
    """
    loads an already loaded config store, it should raise an error.
    """

    with pytest.raises(ConfigurationStoreExistedError):
        config_services.load_configuration('application')


def test_load_configuration_already_loaded_with_ignore():
    """
    loads an already loaded config store with `ignore_on_existed`
    option, it should not raise an error.
    """

    config_services.load_configuration('database', ignore_on_existed=True)


def test_load_configuration_invalid_name():
    """
    loads a config store that does not exist in settings, it should raise an error.
    """

    with pytest.raises(ConfigurationFileNotFoundError):
        config_services.load_configuration('fake_settings')


def test_load_configuration_invalid_name_with_silent():
    """
    loads a config store that does not exist in settings
    with silent option, it should not raise an error.
    """

    config_services.load_configuration('fake_settings_silent', silent=True)


def test_load_configuration_with_interpolation():
    """
    loads a config file which needs interpolation.
    """

    defaults = dict(env_name='test_env', year_num='2020')
    config_services.load_configuration('interpolation', defaults=defaults)
    configs = config_services.get_all('interpolation')

    assert isinstance(configs, dict)
    assert configs.get('name', None) == 'interpolation_config'
    assert configs.get('year', None) == 2020
    assert configs.get('environment', None) == 'test_env'
    assert configs.get('date', None) == date(2020, 12, 10)
    assert configs.get('another_year', None) == 2020


def test_load_configuration_for_all():
    """
    checks all configs have been loaded.
    """

    config_stores = ['alembic',
                     'application',
                     'api',
                     'babel',
                     'communication',
                     'database',
                     'database.binds',
                     'environment',
                     'globalization',
                     'security',
                     'logging']

    for store in config_stores:
        sections = config_services.get_section_names(store)
        assert sections is not None and len(sections) > 0


def test_load_configuration_not_done_for_logging_handlers():
    """
    checks that `logging.handlers` config store not being loaded.
    """

    with pytest.raises(ConfigurationStoreNotFoundError):
        config_services.get_section_names('logging.handlers')


def test_load_configuration_not_done_for_packaging():
    """
    checks that `packaging` config store not being loaded.
    """

    with pytest.raises(ConfigurationStoreNotFoundError):
        config_services.get_section_names('packaging')


def test_load_configuration_not_done_for_pytest_coverage():
    """
    checks that `pytest.coverage` config store not being loaded.
    """

    with pytest.raises(ConfigurationStoreNotFoundError):
        config_services.get_section_names('pytest.coverage')


def test_load_configurations():
    """
    loads given configurations which has not been loaded yet.
    """

    stores = ['store1', 'store2', 'store3']
    try:
        for store in stores:
            create_config_file('{store}.ini'.format(store=store))

        config_services.load_configurations(*stores)

        for store in stores:
            assert config_services.get_section_names(store) is not None
    finally:
        for store in stores:
            delete_config_file('{store}.ini'.format(store=store))


def test_load_configurations_invalid_name():
    """
    loads given configurations which some of them does not have related file.
    it should not raise an error.
    """

    with pytest.raises(ConfigurationFileNotFoundError):
        stores = ['store4', 'store5', 'store6']
        stores_extended = ['store0']
        stores_extended.extend(stores)
        try:
            for store in stores:
                create_config_file('{store}.ini'.format(store=store))

            config_services.load_configurations(*stores_extended)
        finally:
            for store in stores:
                delete_config_file('{store}.ini'.format(store=store))


def test_load_configurations_invalid_name_with_silent():
    """
    loads given configurations which some of them does not have related file.
    with silent option, it should not raise an error.
    """

    stores = ['store7', 'store8', 'store9']
    stores_extended = ['store10']
    stores_extended.extend(stores)
    try:
        for store in stores:
            create_config_file('{store}.ini'.format(store=store))

        config_services.load_configurations(*stores_extended, silent=True)

        for store in stores:
            assert config_services.get_section_names(store) is not None
    finally:
        for store in stores:
            delete_config_file('{store}.ini'.format(store=store))


def test_load_configurations_already_loaded():
    """
    loads given configurations which has been already loaded.
    it should raise an error.
    """

    with pytest.raises(ConfigurationStoreExistedError):
        stores = ['application', 'database']
        config_services.load_configurations(*stores)


def test_load_configurations_already_loaded_with_ignore():
    """
    loads given configurations which has been already loaded with
    `ignore_on_existed` option. it should not raise an error.
    """

    stores = ['application', 'database']
    config_services.load_configurations(*stores, ignore_on_existed=True)


def test_reload():
    """
    reloads the configuration store from it's relevant file.
    it should not raise an error.
    """

    config_services.reload('database')


def test_reload_with_new_interpolation():
    """
    reloads the configuration store from it's relevant
    file which needs interpolation, with new interpolation defaults.
    """

    defaults = dict(env_name='new_test_env', year_num='2000')
    config_services.reload('interpolation', defaults=defaults)
    configs = config_services.get_all('interpolation')

    assert isinstance(configs, dict)
    assert configs.get('name', None) == 'interpolation_config'
    assert configs.get('year', None) == 2000
    assert configs.get('environment', None) == 'new_test_env'
    assert configs.get('date', None) == date(2000, 12, 10)
    assert configs.get('another_year', None) == 2000


def test_reload_with_old_interpolation():
    """
    reloads the configuration store from it's relevant
    file which needs interpolation, with old interpolation defaults.
    """

    config_services.reload('interpolation')
    configs = config_services.get_all('interpolation')

    assert isinstance(configs, dict)
    assert configs.get('name', None) == 'interpolation_config'
    assert configs.get('year', None) == 2000
    assert configs.get('environment', None) == 'new_test_env'
    assert configs.get('date', None) == date(2000, 12, 10)
    assert configs.get('another_year', None) == 2000


def test_reload_for_not_loaded_store():
    """
    reloads the configuration store from it's relevant file.
    the store has not been loaded yet. it should raise an error.
    """

    with pytest.raises(ConfigurationStoreNotFoundError):
        try:
            create_config_file('new_settings_reload.ini')
            config_services.reload('new_settings_reload')
        finally:
            delete_config_file('new_settings_reload.ini')


def test_reload_for_invalid_store():
    """
    reloads the configuration store from it's relevant file which
    is not available in settings. it should raise an error.
    """

    with pytest.raises(ConfigurationStoreNotFoundError):
        config_services.reload('invalid_reload_settings')


def test_get_file_path_database():
    """
    gets the configuration file path for database settings.
    """

    path = config_services.get_file_path('database')
    settings_path = application_services.get_settings_path()
    database_path = os.path.abspath(os.path.join(settings_path, 'database.ini'))
    assert path == database_path


def test_get_file_path_logging():
    """
    gets the configuration file path for logging settings.
    """

    path = config_services.get_file_path('logging')
    settings_path = application_services.get_settings_path()
    logging_path = os.path.abspath(os.path.join(settings_path, 'logging.ini'))
    assert path == logging_path


def test_get_file_path_not_existed():
    """
    gets the configuration file path for a not available
    config store. it should raise an error.
    """

    with pytest.raises(ConfigurationFileNotFoundError):
        config_services.get_file_path('not_available_store')


def test_get_file_path_not_existed_with_silent():
    """
    gets the configuration file path for a not available
    config store with `silent` option. it should not raise an error.
    """

    file_path = config_services.get_file_path('not_available_store', silent=True)
    assert file_path is None


def test_get_default_file_path_with_no_default():
    """
    gets the default configuration file path for a config
    store which does not have a default setting file.
    it should raise an error.
    """

    with pytest.raises(ConfigurationFileNotFoundError):
        config_services.get_default_file_path('interpolation')


def test_get_default_file_path_not_existed():
    """
    gets the default configuration file path for a not
    available config store. it should raise an error.
    """

    with pytest.raises(ConfigurationFileNotFoundError):
        config_services.get_default_file_path('not_available_store')


def test_get_default_file_path_with_no_default_with_silent():
    """
    gets the default configuration file path for a config
    store which does not have a default setting file with
    `silent` option. it should not raise an error.
    """

    file_path = config_services.get_default_file_path('interpolation', silent=True)
    assert file_path is None


def test_get_default_file_path_not_existed_with_silent():
    """
    gets the default configuration file path for a not
    available config store with `silent` option.
    it should not raise an error.
    """

    file_path = config_services.get_default_file_path('not_available_store', silent=True)
    assert file_path is None


def test_get_file_name():
    """
    gets configuration file name for environment config store.
    """

    file_name = config_services.get_file_name('environment')
    assert file_name == 'environment.ini'


def test_get_file_name_not_existed():
    """
    gets configuration file name for a not available config store.
    it should raise an error.
    """

    with pytest.raises(ConfigurationFileNotFoundError):
        config_services.get_file_name('not_available_store')


def test_get_file_name_not_existed_with_silent():
    """
    gets configuration file name for a not available config store
    with `silent` option. it should not raise an error.
    """

    file_name = config_services.get_file_name('not_available_store', silent=True)
    assert file_name is None


def test_create_config_file():
    """
    creates the requested config file from default pyrin configurations.
    """

    name = 'api.ini'
    delete_config_file(name)
    assert_config_file_not_existed(name)
    config_services.create_config_file('api')
    assert_config_file_existed(name)


def test_create_config_file_not_existed():
    """
    creates the requested config file from default pyrin configurations.
    the config file is not available in pyrin default settings and it should
    raise an error.
    """

    with pytest.raises(ConfigurationFileNotFoundError):
        config_services.create_config_file('my_own_config')

    assert_config_file_not_existed('my_own_config.ini')


def test_create_config_file_not_existed_with_silent():
    """
    creates the requested config file from default pyrin configurations.
    the config file is not available in pyrin default settings but because
    of silent option it should not raise an error.
    """

    config_services.create_config_file('my_own_config', silent=True)
    assert_config_file_not_existed('my_own_config.ini')


def test_create_config_file_existed():
    """
    creates the requested config file from default pyrin configurations.
    the config file is already available in application settings.
    it should raise an error.
    """

    with pytest.raises(ConfigurationFileExistedError):
        config_services.create_config_file('api')


def test_create_config_file_existed_with_ignore():
    """
    creates the requested config file from default pyrin configurations.
    the config file is already available in application settings.
    it should ignore the creation of a new file.
    """

    assert_config_file_existed('api.ini')
    config_services.create_config_file('api', ignore_on_existed=True)


def test_create_config_file_existed_with_replace():
    """
    creates the requested config file from default pyrin configurations.
    the config file is already available in application settings.
    it should replace the existing config file.
    """

    assert_config_file_existed('api.ini')
    config_services.create_config_file('api', replace_existing=True)


def test_create_config_files():
    """
    creates the requested config files from default pyrin configurations.
    """

    names = ['api.ini', 'babel.mappings.ini']
    for file in names:
        delete_config_file(file)
        assert_config_file_not_existed(file)

    config_services.create_config_files('api', 'babel.mappings')
    for file in names:
        assert_config_file_existed(file)


def test_get():
    """
    gets the value of specified key from provided section of given config store.
    """

    value = config_services.get('api', 'json', 'json_sort_keys')
    assert value is True


def test_get_from_not_available_store():
    """
    gets the value of specified key from provided section
    of given config store which is not available.
    it should raise an error.
    """

    with pytest.raises(ConfigurationStoreNotFoundError):
        config_services.get('missing_store', 'json', 'json_sort_keys')


def test_get_from_not_available_section():
    """
    gets the value of specified key from provided section
    which is not available in given config store.
    it should raise an error.
    """

    with pytest.raises(ConfigurationStoreSectionNotFoundError):
        config_services.get('application', 'fake_section', 'json_sort_keys')


def test_get_from_not_available_key():
    """
    gets the value of specified key which is not available
    from provided section in given config store.
    it should raise an error.
    """

    with pytest.raises(ConfigurationStoreKeyNotFoundError):
        config_services.get('globalization', 'locale', 'fake_key')


def test_get_from_not_available_key_with_default_value():
    """
    gets the value of specified key which is not available
    from provided section in given config store.
    it should not raise an error and should return the default value.
    """

    value = config_services.get('globalization', 'locale', 'fake_key', default=123)
    assert value == 123


def test_get_for_different_stores():
    """
    checks that different config stores has been loaded with correct values.
    """

    restricted_max_content_length = config_services.get('api', 'general',
                                                        'restricted_max_content_length')
    max_content_length = config_services.get('api', 'general', 'max_content_length')
    assert restricted_max_content_length < max_content_length

    server_name = config_services.get('communication', 'test', 'server_name')
    assert server_name is None

    auto_flush = config_services.get('database', 'request_scoped_session', 'autoflush')
    assert auto_flush is True

    auto_commit = config_services.get('database', 'thread_scoped_session', 'autocommit')
    assert auto_commit is False

    pool = config_services.get('database', 'test', 'sqlalchemy_poolclass')
    assert issubclass(pool, Pool)

    env = config_services.get('environment', 'test', 'env')
    assert env == 'testing'

    locale_dir = config_services.get('globalization', 'locale', 'babel_translation_directories')
    assert locale_dir == 'locale'

    secret_key = config_services.get('security', 'general', 'secret_key')
    assert secret_key is not None

    hs256_key = config_services.get('security', 'token', 'hs256_key')
    assert hs256_key is not None

    rsa256_public_key = config_services.get('security', 'encryption', 'rsa256_public_key')
    assert rsa256_public_key is not None


def test_get_active():
    """
    gets the value of given key from active section of given config store.
    """

    value = config_services.get_active('environment', 'env')
    assert value == 'testing'


def test_get_active_invalid_store():
    """
    gets the value of given key from active section of
    given config store which is unavailable.
    it should raise an error.
    """

    with pytest.raises(ConfigurationStoreNotFoundError):
        config_services.get_active('missing_store', 'env')


def test_get_active_without_active_section():
    """
    gets the value of given key from active section of
    given config store which has no active section.
    it should raise an error.
    """

    with pytest.raises(ConfigurationStoreSectionNotFoundError):
        config_services.get_active('api', 'max_content_length')


def test_get_active_invalid_key():
    """
    gets the value of given key which is unavailable from
    active section of given config store.
    it should raise an error.
    """

    with pytest.raises(ConfigurationStoreKeyNotFoundError):
        config_services.get_active('environment', 'missing_key')


def test_get_active_invalid_key_with_default_value():
    """
    gets the value of given key which is unavailable from
    active section of given config store.
    it should not raise an error and should return the default value.
    """

    value = config_services.get_active('environment', 'missing_key', default=False)
    assert value is False


def test_get_section_names():
    """
    gets all available section names of given config store.
    """

    sections = config_services.get_section_names('communication')
    assert sections is not None
    assert all(name in sections for name in ['active', 'development',
                                             'production', 'test'])


def test_get_section_names_invalid_store():
    """
    gets all available section names of given config store which
    is unavailable. it should raise an error.
    """

    with pytest.raises(ConfigurationStoreNotFoundError):
        config_services.get_section_names('missing_store')


def test_get_section():
    """
    gets all key/values stored in given section of specified config store.
    and checks that all keys are present in loaded section.
    """

    section = config_services.get_section('security', 'token')
    assert section is not None
    assert all(name in section.keys() for name in ['access_token_lifetime',
                                                   'refresh_token_lifetime',
                                                   'hs256_key', 'hs256_key_length',
                                                   'rs256_public_key', 'rs256_private_key',
                                                   'default_token_handler'])


def test_get_section_invalid_store():
    """
    gets all key/values stored in given section of specified config store
    which is unavailable. it should raise an error.
    """

    with pytest.raises(ConfigurationStoreNotFoundError):
        config_services.get_section('missing_store', 'token')


def test_get_section_invalid_section():
    """
    gets all key/values stored in given section which is unavailable
    of specified config store. it should raise an error.
    """

    with pytest.raises(ConfigurationStoreSectionNotFoundError):
        config_services.get_section('application', 'missing_section')


def test_get_section_uppercase_key():
    """
    gets all key/values stored in given section of specified config store.
    it should convert all keys to uppercase.
    """

    section = config_services.get_section('application', 'general',
                                          converter=string_utils.upper)

    assert section is not None
    assert all(name.isupper() for name in section.keys())


def test_get_section_keys():
    """
    gets all available keys in given section of specified config store.
    """

    section_keys = config_services.get_section_keys('database', 'production')
    assert section_keys is not None
    assert all(name in section_keys for name in ['sqlalchemy_case_sensitive',
                                                 'sqlalchemy_encoding',
                                                 'sqlalchemy_isolation_level',
                                                 'sqlalchemy_pool_reset_on_return',
                                                 'sqlalchemy_url'])


def test_get_section_keys_invalid_store():
    """
    gets all available keys in given section of specified config store
    which is unavailable. it should raise an error.
    """

    with pytest.raises(ConfigurationStoreNotFoundError):
        config_services.get_section_keys('missing_store', 'production')


def test_get_section_keys_invalid_section():
    """
    gets all available keys in given section which is unavailable
    of specified config store. it should raise an error.
    """

    with pytest.raises(ConfigurationStoreSectionNotFoundError):
        config_services.get_section_keys('application', 'missing_section')


def test_get_all():
    """
    gets all available key/values from different sections of
    given config store in a flat dict, eliminating the sections.
    """

    values = config_services.get_all('api')
    assert all(name in values.keys() for name in ['max_content_length',
                                                  'restricted_max_content_length',
                                                  'use_x_sendfile',
                                                  'json_as_ascii',
                                                  'json_sort_keys',
                                                  'jsonify_mimetype'])


def test_get_all_from_active():
    """
    gets all available key/values from different sections of
    given config store which has an active section in a flat dict.
    """

    values = config_services.get_all('environment')
    assert all(name in values.keys() for name in ['env',
                                                  'debug',
                                                  'testing',
                                                  'unit_testing'])

    assert values.get('env') == 'testing'


def test_get_all_duplicate_key():
    """
    gets all available key/values from different sections of
    given config store which has a duplicate key in two different sections.
    it should raise an error.
    """

    with pytest.raises(ConfigurationStoreDuplicateKeyError):
        config_services.load_configuration('duplicate.key')
        config_services.get_all('duplicate.key')


def test_get_all_invalid_store():
    """
    gets all available key/values from different sections of
    given config store which is unavailable, it should raise an error.
    """

    with pytest.raises(ConfigurationStoreNotFoundError):
        config_services.get_all('missing_store')


def test_get_all_uppercase_keys():
    """
    gets all available key/values from different sections of
    given config store converted into uppercase keys.
    """

    values = config_services.get_all('application',
                                     converter=string_utils.upper)

    assert all(name in values.keys() for name in ['TITLE',
                                                  'ENCODING',
                                                  'FLASK_LOG_LEVEL'])

    assert values.get('TITLE') == 'pyrin_unit_tests'


def test_get_active_section():
    """
    gets all key/values from the active section available in given config store.
    """

    section = config_services.get_active_section('database')

    assert all(name in section.keys() for name in ['sqlalchemy_case_sensitive',
                                                   'sqlalchemy_echo',
                                                   'sqlalchemy_isolation_level',
                                                   'sqlalchemy_pool_pre_ping'])

    assert section.get('sqlalchemy_poolclass') == StaticPool


def test_get_active_section_no_active():
    """
    gets all key/values from the active section available in
    given config store which has no active section.
    it should raise an error.
    """

    with pytest.raises(ConfigurationStoreSectionNotFoundError):
        config_services.get_active_section('application')


def test_get_active_section_invalid_store():
    """
    gets all key/values from the active section available in
    given config store which is unavailable.
    it should raise an error.
    """

    with pytest.raises(ConfigurationStoreNotFoundError):
        config_services.get_active_section('missing_store')


def test_get_active_section_uppercase_keys():
    """
    gets all key/values from the active section available in
    given config store in uppercase keys.
    """

    section = config_services.get_active_section('communication',
                                                 converter=string_utils.upper)

    assert all(name in section.keys() for name in ['SERVER_NAME',
                                                   'SERVER_HOST',
                                                   'SERVER_PORT',
                                                   'SERVER_PROTOCOL'])

    assert section.get('SERVER_NAME') is None


def test_get_active_section_name():
    """
    gets the name of active section in given config store.
    """

    name = config_services.get_active_section_name('database')
    assert name == 'test'


def test_get_active_section_name_invalid_store():
    """
    gets the name of active section in given config store
    which is not available. it should raise an error.
    """

    with pytest.raises(ConfigurationStoreNotFoundError):
        config_services.get_active_section_name('missing_store')


def test_get_active_section_name_no_active():
    """
    gets the name of active section in given config
    store which has no active section.
    it should raise an error.
    """

    with pytest.raises(ConfigurationStoreSectionNotFoundError):
        config_services.get_active_section('globalization')
