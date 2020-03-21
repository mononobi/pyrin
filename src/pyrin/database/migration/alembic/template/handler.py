# -*- coding: utf-8 -*-
"""
alembic template handler module.
"""

import os

import pyrin.application.services as application_services

from pyrin.core.structs import DTO
from pyrin.database.migration.alembic.enumerations import AlembicCLIHandlersEnum
from pyrin.template.decorators import template_handler
from pyrin.template.handlers.base import TemplateHandlerBase
from pyrin.database.migration.alembic import AlembicPackage


@template_handler()
class AlembicTemplateHandler(TemplateHandlerBase):
    """
    alembic template handler class.
    """

    def __init__(self):
        """
        initializes an instance of AlembicTemplateHandler.
        """

        pyrin_path = application_services.get_pyrin_main_package_path()
        target = application_services.get_migrations_path()
        source = os.path.abspath(os.path.join(pyrin_path, 'database', 'migration',
                                              'alembic', 'template', 'files'))

        super().__init__(AlembicCLIHandlersEnum.ENABLE, source, target)

    def _get_file_patterns(self):
        """
        gets the file patterns that should be included in replacement operation.

        :rtype: list[str]
        """

        return ['.py']

    def _get_data(self):
        """
        gets the data required in template generation to replace in files.

        :rtype: dict
        """

        return DTO(MIGRATIONS_PATH=application_services.get_migrations_path(),
                   APPLICATION_CLASS=application_services.get_class_name(),
                   APPLICATION_MODULE=application_services.get_module_name())

    def _get_config_stores(self):
        """
        gets the config store names which belong to this template.

        :rtype: list[str]
        """

        return AlembicPackage.CONFIG_STORE_NAMES

    def _get_required_directories(self):
        """
        gets the required directory names that must be created in target path.

        :rtype: list[str]
        """

        return ['sql', 'versions']
