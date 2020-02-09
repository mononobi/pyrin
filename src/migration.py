# -*- coding: utf-8 -*-
"""
pyrin migration module.
"""

import os
import sys

import fire

os.environ['PYTHONPATH'] = os.path.abspath('.')
sys.path.append(os.path.abspath('.'))

from pyrin.database.migration.alembic.cli import AlembicCLI

from tests import PyrinTestApplication


app_instance = PyrinTestApplication(scripting_mode=True)


if __name__ == '__main__':
    fire.Fire(AlembicCLI())
