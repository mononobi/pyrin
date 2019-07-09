# -*- coding: utf-8 -*-
"""
main entry point for pyrin test server.
"""

import os

import pytest

import pyrin.utils.path as path_utils

from tests import PyrinTestApplication


def cleanup():
    """
    cleanups pytest caches after running all tests.
    """

    root_path = path_utils.resolve_application_root_path()
    cache_path = os.path.join(root_path, '.pytest_cache')
    command = 'rm -r {path}'.format(path=cache_path)
    os.system(command)


# the if condition is to ensure that multiprocessing
# on windows works as expected.
if __name__ == '__main__':
    app = PyrinTestApplication()
    pytest.main()
    cleanup()
