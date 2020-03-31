# -*- coding: utf-8 -*-
"""
manage_unit module.

to enable locale management for unit tests, execute:
`python manage.py babel enable`

to enable migrations for unit tests, execute:
`python manage.py alembic enable`

to create a new package for unit tests, execute:
`python manage.py template package`
"""

import fire

from pyrin.database.migration.alembic.cli import AlembicCLI
from pyrin.globalization.locale.babel.cli import BabelCLI
from pyrin.template.cli import TemplateCLI

from tests.unit import PyrinUnitTestApplication


app_instance = PyrinUnitTestApplication(import_name='tests.unit',
                                        scripting_mode=True)


class Groups(object):
    """
    groups class.

    each cli handler group is resided in its relevant group name.

    usage example:

    `python manage.py alembic upgrade --arg value`
    `python manage.py babel extract --arg value`
    `python manage.py template package`
    """

    def __init__(self):
        """
        initializes an instance of Groups.
        """

        self.babel = BabelCLI()
        self.alembic = AlembicCLI()
        self.template = TemplateCLI()


if __name__ == '__main__':
    fire.Fire(Groups())
