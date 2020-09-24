# -*- coding: utf-8 -*-
"""
manage unit module.

to enable locale management for unit tests, execute:
`python manage.py babel enable`

to enable migrations for unit tests, execute:
`python manage.py alembic enable`

to create a new package for unit tests, execute:
`python manage.py template package`

usage example:

`python manage.py alembic upgrade --arg value`
`python manage.py babel extract --arg value`
`python manage.py template package`
`python manage.py celery worker --arg value`
`python manage.py security token --arg value`
"""

import fire

from pyrin.cli.services import get_cli_groups

from tests.unit import PyrinUnitTestApplication


app_instance = PyrinUnitTestApplication(import_name='tests.unit',
                                        scripting_mode=True)


if __name__ == '__main__':
    fire.Fire(get_cli_groups())
