# -*- coding: utf-8 -*-
"""
start tests module.
"""

import os

import pytest

import pyrin.database.migration.services as migration_services
import pyrin.application.services as application_services
import pyrin.configuration.services as config_services

from pyrin.utils.custom_print import print_warning, print_info

from tests import PyrinTestApplication


def remove(name):
    """
    removes a file or directory by specified name from application root directory.

    :param str name: name of the file or directory to be removed.
    """

    root_path = application_services.get_application_root_path()
    file_path = os.path.join(root_path, name)
    file_path = os.path.abspath(file_path)

    if os.path.exists(file_path):
        command = 'rm -r {path}'.format(path=file_path)
        os.system(command)
    else:
        print_info('Path [{file}] does not exist.'.format(file=file_path))


def cleanup():
    """
    cleanups the environment after running all tests.
    """

    drop_schema()
    remove_coverage()
    remove_pytest_cache()


def remove_pytest_cache():
    """
    removes pytest cache directory.
    """

    remove('.pytest_cache')


def remove_coverage():
    """
    removes coverage file.
    """

    remove('.coverage')


def drop_schema():
    """
    drops all database models.
    """

    print_warning('Dropping all models...')
    migration_services.drop_all()


def start_tests(coverage=False):
    """
    starts tests.

    :param bool coverage: specifies that tests should run with coverage support.
                          note that for debugging tests, it might be required to
                          start tests without coverage.
    """

    args = []
    if coverage is True:
        config_file = config_services.get_file_path('pytest.coverage')
        args = ['--cache-clear',
                '--cov-config={config_file}'.format(config_file=config_file),
                '--cov=pyrin']

    pytest.main(args)
    cleanup()


# the if condition is to ensure that multiprocessing
# on windows works as expected.
if __name__ == '__main__':
    app = PyrinTestApplication()
    start_tests(coverage=True)
