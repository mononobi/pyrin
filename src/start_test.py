# -*- coding: utf-8 -*-
"""
main entry point for pyrin test server.
"""

import pytest

from tests import PyrinTestApplication


# the if condition is to ensure that multiprocessing
# on windows works as expected.
if __name__ == '__main__':
    app = PyrinTestApplication()
    pytest.main()
