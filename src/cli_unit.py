# -*- coding: utf-8 -*-
"""
cli unit module.

to enable locale management for unit tests, execute:
`python cli.py babel enable`

to enable migrations for unit tests, execute:
`python cli.py alembic enable`

to create a new package for unit tests, execute:
`python cli.py template package`

usage example:

`python cli.py alembic upgrade --arg value`
`python cli.py babel extract --arg value`
`python cli.py template package`
`python cli.py celery worker --arg value`
`python cli.py security token --arg value`
"""

import fire

from pyrin.cli.services import get_cli_groups

from tests.unit import PyrinUnitTestApplication


app_instance = PyrinUnitTestApplication(import_name='tests.unit',
                                        scripting_mode=True)

if __name__ == '__main__':
    fire.Fire(get_cli_groups())
