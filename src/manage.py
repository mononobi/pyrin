# -*- coding: utf-8 -*-
"""
manage module.
"""

import fire

from pyrin.database.migration.alembic.cli import AlembicCLI
from pyrin.globalization.locale.babel.cli import BabelCLI

from tests import PyrinTestApplication


app_instance = PyrinTestApplication(scripting_mode=True)


class Groups(object):
    """
    groups class.
    each cli handler group is resided inside its relevant group name.
    usage example:
    `python manage.py alembic upgrade --input value`
    `python manage.py babel extract --input value`
    """

    def __init__(self):
        """
        initializes an instance of Groups.
        """

        self.babel = BabelCLI()
        self.alembic = AlembicCLI()


if __name__ == '__main__':
    fire.Fire(Groups())
