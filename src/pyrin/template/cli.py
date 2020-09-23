# -*- coding: utf-8 -*-
"""
template cli module.
"""

import pyrin.template.services as template_services

from pyrin.cli.decorators import cli_invoke, cli_group
from pyrin.core.structs import CLI
from pyrin.template.enumerations import TemplateCLIHandlersEnum


@cli_group('template')
class TemplateCLI(CLI):
    """
    template cli class.

    this class exposes all template cli commands.
    """

    @cli_invoke
    def package(self, **options):
        """
        create a new package for application.

        inputs could be provided within command itself, as well as
        through interactive mode if not provided within command.

        :keyword str package_path: the new package path. it must be a relative
                                   path inside application main package path.

        :keyword str package_class_name: the new package class name.

        :keyword bool help: show the help message for this command.
                            defaults to False if not provided.
        """

        return template_services.create(TemplateCLIHandlersEnum.PACKAGE, **options)

    @cli_invoke
    def empty_package(self, **options):
        """
        create a new empty package for application.

        inputs could be provided within command itself, as well as
        through interactive mode if not provided within command.

        :keyword str package_path: the new package path. it must be a relative
                                   path inside application main package path.

        :keyword str package_class_name: the new package class name.

        :keyword bool help: show the help message for this command.
                            defaults to False if not provided.
        """

        return template_services.create(TemplateCLIHandlersEnum.EMPTY_PACKAGE, **options)
