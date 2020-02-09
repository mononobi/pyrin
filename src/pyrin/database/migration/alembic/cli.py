# -*- coding: utf-8 -*-
"""
database migration alembic cli module.
"""

from pyrin.cli.decorators import cli
from pyrin.core.context import CLI
from pyrin.utils.datetime import get_current_timestamp


class AlembicCLI(CLI):
    """
    alembic cli class.
    this class exposes all alembic cli commands.
    """

    @cli
    def branches(self, verbose=False, help=False):
        """
        show current branch points.

        :param bool verbose: use more verbose output.
        :param bool help: show the help message for this command.
        """
        pass

    @cli
    def current(self, verbose=False, help=False):
        """
        display the current revision for a database.

        :param bool verbose: use more verbose output.
        :param bool help: show the help message for this command.
        """
        pass

    @cli
    def downgrade(self, revision=None, sql=False, tag=None, help=False):
        """
        revert to a previous version.
        use `base` to revert all revisions.

        :param str revision: revision identifier.

        :param bool sql: don't emit sql to database, dump to standard
                         output/file instead. see docs on offline mode.

        :param str tag: arbitrary `tag` name. can be used
                        by custom `env.py` scripts.

        :param bool help: show the help message for this command.
        """
        pass

    @cli
    def heads(self, resolve_dependencies=False, verbose=False, help=False):
        """
        show current available heads in the script directory.

        :param bool resolve_dependencies: treat dependency versions as down revisions.
        :param bool verbose: use more verbose output.
        :param bool help: show the help message for this command.
        """
        pass

    @cli
    def history(self, revision_range=None, indicate_current=False,
                verbose=False, help=False):
        """
        list changeset scripts in chronological order.

        :param str revision_range: specify a revision range.
                                   format is [start]:[end]

        :param bool indicate_current: indicate the current revision.
        :param bool verbose: use more verbose output.
        :param bool help: show the help message for this command.
        """
        pass

    @cli
    def merge(self, revisions=None, message=None,
              branch_label=None, revision_id=None, help=False):
        """
        merge two revisions together. creates a new migration file.

        :param Union[str, list[str]] revisions: one or more revisions,
                                                or `heads` for all heads.

        :param str message: message string to use with `revision`.

        :param str branch_label: specify a branch label to
                                 apply to the new revision.

        :param str revision_id: specify a hardcoded revision
                                id instead of generating one.

        :param bool help: show the help message for this command.
        """

        if message is None:
            message = get_current_timestamp()

        return dict(message=message)

    @cli
    def revision(self, message=None, autogenerate=True, sql=False,
                 head=None, splice=False, branch_label=None, version_path=None,
                 revision_id=None, depends_on=None, help=False):
        """
        create a new revision file.

        :param str message: message string to use with `revision`.

        :param bool autogenerate: populate revision script with candidate migration
                                  operations, based on comparison of database to model.

        :param bool sql: don't emit sql to database, dump to standard
                         output/file instead. see docs on offline mode.

        :param str head: specify head revision or <branchname>@head
                         to base new revision on.

        :param bool splice: allow a non-head revision as the `head` to splice onto.

        :param str branch_label: specify a branch label to
                                 apply to the new revision.

        :param str version_path: specify specific path from config for version file.
        :param str revision_id: specify a hardcoded revision id instead of generating one.

        :param Union[str, list[str]] depends_on: specify one or more revision identifiers
                                                 which this revision should depend on.

        :param bool help: show the help message for this command.
        """

        if message is None:
            message = get_current_timestamp()

        return dict(message=message)

    @cli
    def show(self, revision=None, help=False):
        """
        show the revision(s) denoted by the given symbol.

        :param str revision: revision identifier.
                             it could be a part of revision identifier
                             to filter all matching revisions.

        :param bool help: show the help message for this command.
        """
        pass

    @cli
    def stamp(self, revisions=None, sql=False, tag=None, purge=False, help=False):
        """
        stamp the revision table with the given revision(s).
        don't run any migrations.

        :param Union[str, list[str]] revisions: one or more revisions,
                                                or `heads` for all heads.

        :param bool sql: don't emit sql to database, dump to standard
                         output/file instead. see docs on offline mode.

        :param str tag: arbitrary `tag` name. can be used
                        by custom `env.py` scripts.

        :param bool purge: unconditionally erase the version table before stamping.
        :param bool help: show the help message for this command.
        """
        pass

    @cli
    def upgrade(self, revision=None, sql=False, tag=None, help=False):
        """
        upgrade to a later version.
        use `head` to upgrade to latest revision.

        :param str revision: revision identifier.

        :param bool sql: don't emit sql to database, dump to standard
                         output/file instead. see docs on offline mode.

        :param str tag: arbitrary `tag` name. can be used
                        by custom `env.py` scripts.

        :param bool help: show the help message for this command.
        """
        pass
