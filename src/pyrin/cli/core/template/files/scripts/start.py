# -*- coding: utf-8 -*-
"""
start module.
"""

from APPLICATION_PACKAGE import APPLICATION_CLASS


app = APPLICATION_CLASS()

# the if condition is to ensure that multiprocessing
# on windows works as expected.
if __name__ == '__main__':
    app.run(use_reloader=False)
