# -*- coding: utf-8 -*-
"""
template cli module.
"""

import pyrin.template.services as template_services

from pyrin.cli.decorators import cli_invoke
from pyrin.core.structs import CLI
from pyrin.template.enumerations import TemplateCLIHandlersEnum


class TemplateCLI(CLI):
    """
    template cli class.
    this class exposes all template cli commands.
    """

    @cli_invoke
    def package(self, help=False):
        """
        create a new package for application.

        :keyword bool help: show the help message for this command.
                            defaults to False if not provided.
        """

        return template_services.create(TemplateCLIHandlersEnum.PACKAGE)

    @cli_invoke
    def empty_package(self, help=False):
        """
        create a new empty package for application.

        :keyword bool help: show the help message for this command.
                            defaults to False if not provided.
        """

        return template_services.create(TemplateCLIHandlersEnum.EMPTY_PACKAGE)
