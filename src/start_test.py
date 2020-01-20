# -*- coding: utf-8 -*-
"""
main entry point for pyrin test server.
"""

import os

import pytest

from pyrin.utils.custom_print import print_warning
from pyrin.utils.path import resolve_application_root_path

from tests import PyrinTestApplication


def cleanup():
    """
    cleanups the environment after running all tests.
    """

    drop_schema()
    remove_cache()


def remove_cache():
    """
    removes pytest cache directory.
    """

    root_path = resolve_application_root_path()
    cache_path = os.path.join(root_path, '.pytest_cache')
    command = 'rm -r {path}'.format(path=cache_path)
    os.system(command)


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
    pytest.main()
    cleanup()
