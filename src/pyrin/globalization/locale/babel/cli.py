# -*- coding: utf-8 -*-
"""
babel cli module.
"""

import pyrin.globalization.locale.babel.services as babel_services

from pyrin.cli.decorators import cli, cli_invoke, cli_group
from pyrin.core.structs import CLI


@cli_group('babel')
class BabelCLI(CLI):
    """
    babel cli class.

    this class exposes all babel cli commands.
    """

    _execute_service = babel_services.execute

    @cli_invoke
    def enable(self, include_pyrin=True, include_app=True, **options):
        """
        enables locale management for the application.

        :keyword bool include_pyrin: specifies that it should extract pyrin localizable
                                     messages. defaults to True if not provided.

        :keyword bool include_app: specifies that it should extract application
                                   localizable messages. defaults to True if not provided.

        :keyword bool help: show the help message for this command.
                            defaults to False if not provided.
        """

        return babel_services.enable(include_pyrin, include_app)

    @cli_invoke
    def rebuild(self, include_pyrin=True, include_app=True, **options):
        """
        it will do the three complete steps needed to
        update and compile locales with new messages.

        it will do:
            1. extract
            2. update
            3. compile

        this command is defined for convenient of usage, but if you need
        to do these steps separately, you could ignore this command and
        use the relevant command for each step.

        :keyword bool include_pyrin: specifies that it must extract pyrin localizable
                                     messages as well. defaults to True if not provided.

        :keyword bool include_app: specifies that it must extract application localizable
                                   messages as well. defaults to True if not provided.

        :keyword str locale: locale name of the catalog to compile.
                             it will compile all catalogs if not provided.

        :keyword bool help: show the help message for this command.
                            defaults to False if not provided.
        """

        return babel_services.rebuild(include_pyrin, include_app, **options)

    @cli
    def init(self, locale, **options):
        """
        create new message catalogs from a `.pot` file.

        :param str locale: locale name for the new localized catalog.
                           for example: `en` or `fr` or ...

        :keyword bool help: show the help message for this command.
                            defaults to False if not provided.
        """

        return babel_services.check_init(locale)

    @cli
    def update(self, **options):
        """
        update existing message catalogs from a `.pot` file.

        :keyword str locale: locale name of the catalog to compile.
                             it will compile all catalogs if not provided.

        :keyword bool help: show the help message for this command.
                            defaults to False if not provided.
        """
        pass

    @cli
    def extract(self, include_pyrin=True, include_app=True, **options):
        """
        extract messages from source files and generate a `.pot` file.

        :keyword bool include_pyrin: specifies that it must extract pyrin localizable
                                     messages as well. defaults to True if not provided.

        :keyword bool include_app: specifies that it must extract application localizable
                                   messages as well. defaults to True if not provided.

        :keyword bool help: show the help message for this command.
                            defaults to False if not provided.
        """
        pass

    @cli
    def compile(self, **options):
        """
        compile message catalogs to `.mo` files.

        :keyword str locale: locale name of the catalog to compile.
                             it will compile all catalogs if not provided.

        :keyword bool statistics: print statistics about translations.
                                  defaults to False if not provided.

        :keyword bool help: show the help message for this command.
                            defaults to False if not provided.
        """
        pass
