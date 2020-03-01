# -*- coding: utf-8 -*-
"""
manage module.
"""

import fire

from pyrin.database.migration.alembic.cli import AlembicCLI

from tests import PyrinTestApplication


app_instance = PyrinTestApplication(scripting_mode=True)


if __name__ == '__main__':
    fire.Fire(AlembicCLI())
