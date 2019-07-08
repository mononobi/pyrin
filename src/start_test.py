# -*- coding: utf-8 -*-
"""
main entry point for pyrin test server.
"""

from tests import PyrinTestApplication

# the if condition is to ensure that multiprocessing
# on windows works as expected.
if __name__ == '__main__':
    app = PyrinTestApplication()
    app.run(use_reloader=False)
