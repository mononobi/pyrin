# -*- coding: utf-8 -*-
"""
main entry point for pyrin test server.
"""

import os

import pytest

from pyrin.utils.custom_print import print_warning
from pyrin.utils.path import resolve_application_root_path

from tests import PyrinTestApplication


def remove(name):
    """
    removes a file or directory by specified name from application root directory.

    :param str name: name of the file or directory to be removed.
    """

    root_path = resolve_application_root_path()
    file_path = os.path.join(root_path, name)
    command = 'rm -r {path}'.format(path=file_path)
    os.system(command)


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

    import pyrin.database.services as database_services

    print_warning('Dropping all models...')
    database_services.drop_all()


# the if condition is to ensure that multiprocessing
# on windows works as expected.
if __name__ == '__main__':
    app = PyrinTestApplication()
    pytest.main(['--cov-config=tests/settings/pytest.coverage.config',
                 '--cov=pyrin'])
    cleanup()
