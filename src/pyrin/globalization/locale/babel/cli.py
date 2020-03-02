# -*- coding: utf-8 -*-
"""
babel cli module.
"""

import pyrin.globalization.locale.babel.services as babel_services

from pyrin.cli.decorators import cli
from pyrin.core.context import CLI


class BabelCLI(CLI):
    """
    babel cli class.
    this class exposes all babel cli commands.
    """

    _execute_service = babel_services.execute

    @cli
    def init(self, help=False):
        """
        create new message catalogs from a `.pot` file.

        :keyword bool verbose: use more verbose output.
                               defaults to False if not provided.

        :keyword bool help: show the help message for this command.
                            defaults to False if not provided.
        """
        pass

    @cli
    def update(self, help=False):
        """
        update existing message catalogs from a `.pot` file.

        :keyword bool verbose: use more verbose output.
                               defaults to False if not provided.

        :keyword bool help: show the help message for this command.
                            defaults to False if not provided.
        """
        pass

    @cli
    def extract(self, help=False):
        """
        extract messages from source files and generate a `.pot` file.

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
    def compile(self, help=False):
        """
        compile message catalogs to `.mo` files.

        :keyword bool resolve_dependencies: treat dependency versions as down revisions.
                                            defaults to False if not provided.

        :keyword bool verbose: use more verbose output.
                               defaults to False if not provided.

        :keyword bool help: show the help message for this command.
                            defaults to False if not provided.
        """
        pass

    @cli
    def rebuild(self, help=False):
        """
        it will do the three complete steps to update and
        compile locales with new messages.

        it will do:
            1. extract
            2. update
            3. compile

        this command is defined for convenient of usage, but if you need
        to do these steps separately, you could ignore this command and
        use the relevant command for each step.

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
