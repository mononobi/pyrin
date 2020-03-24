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
    def package(self, package_path=None, package_class_name=None, help=False):
        """
        create a new package for application.

        inputs could be provided within command itself, as well as
        through interactive mode if not provided within command.

        :param str package_path: the new package path. it must be a relative
                                 path inside application main package path.

        :param str package_class_name: the new package class name.

        :keyword bool help: show the help message for this command.
                            defaults to False if not provided.
        """

        return template_services.create(TemplateCLIHandlersEnum.PACKAGE,
                                        package_path, package_class_name)

    @cli_invoke
    def empty_package(self, package_path=None,
                      package_class_name=None, help=False):
        """
        create a new empty package for application.

        inputs could be provided within command itself, as well as
        through interactive mode if not provided within command.

        :param str package_path: the new package path. it must be a relative
                                 path inside application main package path.

        :param str package_class_name: the new package class name.

        :keyword bool help: show the help message for this command.
                            defaults to False if not provided.
        """

        return template_services.create(TemplateCLIHandlersEnum.EMPTY_PACKAGE,
                                        package_path, package_class_name)
