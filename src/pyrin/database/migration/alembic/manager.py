# -*- coding: utf-8 -*-
"""
database migration alembic manager module.
"""

from pyrin.core.context import Manager, DTO
from pyrin.utils.path import resolve_application_root_path


class DatabaseMigrationAlembicManager(Manager):
    """
    database migration alembic manager class.
    """

    DEFAULT_ENGINE_NAME = 'default'

    def __init__(self):
        """
        initializes an instance of DatabaseMigrationManager.
        """

        super().__init__()

        # a dictionary containing cli handlers
        # for different alembic commands.
        # in the form of: {str command name: CLIHandlerBase handler}
        self.command_handlers = DTO()

    def revision(self, message=None, autogenerate=True, sql=None,
                 head=None, splice=None, branch_label=None,
                 version_path=None, rev_id=None, depends_on=None):
        """
        makes a revision for available databases.

        :param str message: message string to use with 'revision'.

        :param bool autogenerate: populate revision script with candidate migration
                                  operations, based on comparison of database to model.


        :param bool sql: don't emit sql to database, just dump to standard
                         output/file instead. see docs on offline mode.

        :param str head: specify head revision or <branchname>@head to base new
                         revision on.

        :param bool splice: allow a non-head revision as the 'head' to splice onto.
        :param str branch_label: specify a branch label to apply to the new revision.
        :param str version_path: specify specific path from config for version file.
        :param str rev_id: specify a hardcoded revision id instead of generating one.

        :param Union[str, list[str]] depends_on: specify one or more revision identifiers
                                                 which this revision should depend on.
        """
        try:
            print(autogenerate)
            command = ['alembic',
                       '-c', settings_file,
                       'revision', '--autogenerate']
            subprocess.check_call(command)
        except CalledProcessError as error:
            print_warning(str(error), True)

    def current(self):
        command = ['alembic',
                   '-c', settings_file,
                   'current', '-v']
        subprocess.check_call(command)

    def upgrade(self):
        command = 'alembic upgrade head'
        subprocess.check_call(command)