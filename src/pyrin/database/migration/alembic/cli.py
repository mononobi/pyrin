# -*- coding: utf-8 -*-
"""
alembic cli module.
"""

import pyrin.database.migration.alembic.services as alembic_services

from pyrin.cli.decorators import cli, cli_invoke, cli_group
from pyrin.core.structs import CLI


@cli_group('alembic')
class AlembicCLI(CLI):
    """
    alembic cli class.

    this class exposes all alembic cli commands.
    """

    _execute_service = alembic_services.execute

    @cli_invoke
    def enable(self, **options):
        """
        enable migrations for application.

        :keyword bool help: show the help message for this command.
                            defaults to False if not provided.
        """

        return alembic_services.enable()

    @cli
    def branches(self, **options):
        """
        show current branch points.

        :keyword bool verbose: use more verbose output.
                               defaults to False if not provided.

        :keyword bool help: show the help message for this command.
                            defaults to False if not provided.
        """
        pass

    @cli
    def current(self, **options):
        """
        display the current revision for a database.

        :keyword bool verbose: use more verbose output.
                               defaults to False if not provided.

        :keyword bool help: show the help message for this command.
                            defaults to False if not provided.
        """
        pass

    @cli
    def downgrade(self, revision, **options):
        """
        revert to a previous version.
        use `base` to revert all revisions.

        :param str revision: revision identifier.

        :keyword bool sql: don't emit sql to database, dump to standard
                           output/file instead. see docs on offline mode.
                           defaults to False if not provided.

        :keyword str tag: arbitrary `tag` name. can be used
                          by custom `env.py` scripts.

        :keyword bool help: show the help message for this command.
                            defaults to False if not provided.
        """
        pass

    @cli
    def heads(self, **options):
        """
        show current available heads in the script directory.

        :keyword bool resolve_dependencies: treat dependency versions as down revisions.
                                            defaults to False if not provided.

        :keyword bool verbose: use more verbose output.
                               defaults to False if not provided.

        :keyword bool help: show the help message for this command.
                            defaults to False if not provided.
        """
        pass

    @cli
    def history(self, **options):
        """
        list change-set scripts in chronological order.

        :keyword str revision_range: specify a revision range.
                                     format is [start]:[end]

        :keyword bool indicate_current: indicate the current revision.
                                        defaults to False if not provided.

        :keyword bool verbose: use more verbose output.
                               defaults to False if not provided.

        :keyword bool help: show the help message for this command.
                            defaults to False if not provided.
        """
        pass

    @cli
    def merge(self, revisions, **options):
        """
        merge two revisions together. creates a new migration file.

        :param str | list[str] revisions: one or more revisions,
                                          or `heads` for all heads.

        :keyword str message: message string to use with `revision`.
                              defaults to current timestamp if not provided.

        :keyword str branch_label: specify a branch label to
                                   apply to the new revision.

        :keyword str revision_id: specify a hardcoded revision
                                  id instead of generating one.

        :keyword bool help: show the help message for this command.
                            defaults to False if not provided.
        """
        pass

    @cli
    def revision(self, **options):
        """
        create a new revision file.

        :keyword str message: message string to use with `revision`.
                              defaults to current timestamp if not provided.

        :keyword bool autogenerate: populate revision script with candidate migration
                                    operations, based on comparison of database to model.
                                    defaults to True if not provided.

        :keyword bool sql: don't emit sql to database, dump to standard
                           output/file instead. see docs on offline mode.
                           defaults to False if not provided.

        :keyword str head: specify head revision or <branchname>@head
                           to base new revision on.

        :keyword bool splice: allow a non-head revision as the `head` to splice onto.
                              defaults to False if not provided.

        :keyword str branch_label: specify a branch label to
                                   apply to the new revision.

        :keyword str version_path: specify specific path from config for version file.
        :keyword str revision_id: specify a hardcoded revision id instead of generating one.

        :keyword str | list[str] depends_on: specify one or more revision identifiers
                                             which this revision should depend on.

        :keyword bool help: show the help message for this command.
                            defaults to False if not provided.
        """
        pass

    @cli
    def show(self, revision, **options):
        """
        show the revision(s) denoted by the given symbol.

        :param str revision: revision identifier.
                             it could be a part of revision identifier
                             to filter all matching revisions.

        :keyword bool help: show the help message for this command.
                            defaults to False if not provided.
        """
        pass

    @cli
    def stamp(self, revisions, **options):
        """
        stamp the revision table with the given revision(s).
        don't run any migrations.

        :param str | list[str] revisions: one or more revisions,
                                          or `heads` for all heads.

        :keyword bool sql: don't emit sql to database, dump to standard
                           output/file instead. see docs on offline mode.
                           defaults to False if not provided.

        :keyword str tag: arbitrary `tag` name. can be used
                          by custom `env.py` scripts.

        :keyword bool purge: unconditionally erase the version table before stamping.
                             defaults to False if not provided.

        :keyword bool help: show the help message for this command.
                            defaults to False if not provided.
        """
        pass

    @cli
    def upgrade(self, revision, **options):
        """
        upgrade to a later version.
        use `head` to upgrade to latest revision.

        :param str revision: revision identifier.

        :keyword bool sql: don't emit sql to database, dump to standard
                           output/file instead. see docs on offline mode.
                           defaults to False if not provided.

        :keyword str tag: arbitrary `tag` name. can be used
                          by custom `env.py` scripts.

        :keyword bool help: show the help message for this command.
                            defaults to False if not provided.
        """
        pass
