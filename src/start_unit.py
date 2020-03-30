# -*- coding: utf-8 -*-
"""
start_unit module.
"""

import os

import pytest

import pyrin.database.migration.services as migration_services
import pyrin.application.services as application_services
import pyrin.configuration.services as config_services

from pyrin.utils.custom_print import print_warning, print_info

from tests.unit import PyrinUnitTestApplication


def remove(*name):
    """
    removes a file or directory by specified name from application root directory.

    :param str name: name of the file or directory to be removed.
                     it could be multiple related names to form a
                     relative path.
    """

    root_path = os.path.abspath('.')
    file_path = os.path.join(root_path, *name)
    file_path = os.path.abspath(file_path)

    if os.path.exists(file_path):
        command = 'rm -r {path}'.format(path=file_path)
        os.system(command)
    else:
        print_info('Path [{file}] does not exist.'.format(file=file_path))


def cleanup(coverage):
    """
    cleanups the environment after running all tests.

    :param bool coverage: indicates that coverage file should be cleared.
    """

    drop_schema()
    remove_pytest_cache()

    if coverage is True:
        remove_coverage()


def remove_pytest_cache():
    """
    removes pytest cache directory.
    """

    remove('tests', 'unit', '.pytest_cache')


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

    root_path = application_services.get_application_main_package_path()
    args = ['--cache-clear',
            '--rootdir', root_path,
            '--pyargs', 'tests.unit']
    if coverage is True:
        config_file = config_services.get_file_path('pytest.coverage')
        args.extend(['--cov-config={config_file}'.format(config_file=config_file),
                     '--cov=pyrin'])

    pytest.main(args)
    cleanup(coverage)


# the if condition is to ensure that multiprocessing
# on windows works as expected.
if __name__ == '__main__':
    app = PyrinUnitTestApplication(import_name='tests.unit')
    start_tests(coverage=True)
