# -*- coding: utf-8 -*-
"""
template handlers base module.
"""

import os

import pyrin.configuration.services as config_services
import pyrin.utils.path as path_utils
import pyrin.utils.file as file_utils

from pyrin.utils.custom_print import print_default
from pyrin.template.interface import AbstractTemplateHandler
from pyrin.template.exceptions import TemplateHandlerNameRequiredError, \
    InvalidSourceDirectoryError, InvalidTargetDirectoryError, \
    TemplateTargetDirectoryAlreadyExistedError


class TemplateHandlerBase(AbstractTemplateHandler):
    """
    template handler base class.

    all template handlers must be subclassed from this.
    """

    def __init__(self, name, source, target, **options):
        """
        initializes an instance of TemplateHandlerBase.

        :param str name: name of the handler.
                         each handler must have a unique name.

        :param str source: source directory of template files.

        :param str target: target directory in which template
                           files must be created in.

        :raises TemplateHandlerNameRequiredError: template handler name required error.
        :raises InvalidSourceDirectoryError: invalid source directory error.
        :raises InvalidTargetDirectoryError: invalid target directory error.
        """

        super().__init__()

        if name in (None, '') or name.isspace():
            raise TemplateHandlerNameRequiredError('Template handler name is required.')

        if source in (None, '') or source.isspace() or \
                not os.path.isabs(source) or not os.path.exists(source) or \
                not os.path.isdir(source):
            raise InvalidSourceDirectoryError('The specified source directory is invalid.')

        if target in (None, '') or target.isspace() or not os.path.isabs(target):
            raise InvalidTargetDirectoryError('The specified target directory is invalid.')

        self._name = name
        self._source = source
        self._target = target
        self._config_stores = self._get_config_stores()
        self._data = self._get_data()

    def create(self):
        """
        creates the template files in target path of this handler.

        :raises TemplateTargetDirectoryAlreadyExistedError: template target directory
                                                            already existed error.
        """

        self._validate_target()
        self._copy_config_files()
        self._copy_template_files()
        self._replace_config_values()
        self._replace_template_values()
        self._finalize()

        self._print_info('Template has been created in [{target}].'
                         .format(target=self._target))

    def _validate_target(self):
        """
        validates target path for template creation.

        it assures that target path does not exist, but subclasses could
        override this method if different type of validation is required.

        :raises TemplateTargetDirectoryAlreadyExistedError: template target directory
                                                            already existed error.
        """

        if os.path.exists(self._target):
            raise TemplateTargetDirectoryAlreadyExistedError('Target directory [{dir}] is '
                                                             'already existed. if you want '
                                                             'to regenerate this template, '
                                                             'you should delete the existing '
                                                             'directory first.'
                                                             .format(dir=self._target))

    def _copy_config_files(self):
        """
        copies any required config files for current template handler.
        """

        config_services.create_config_files(*self._config_stores, ignore_on_existed=True)

    def _copy_template_files(self):
        """
        copies required template files from source path to target path of this handler.
        """

        path_utils.copy_directory(self._source, self._target)

    def _replace_config_values(self):
        """
        replaces the values of config files with values in given dict.
        """

        if self._data is not None:
            for store in self._config_stores:
                config_path = config_services.get_file_path(store)
                file_utils.replace_file_values(config_path, self._data)

    def _replace_template_values(self):
        """
        replaces the values of files in target directory with values in given dict.
        """

        if self._data is not None:
            file_utils.replace_files_values(self._target, self._data,
                                            *self._get_file_patterns())

    def _get_file_patterns(self):
        """
        gets the file patterns that should be included in replacement operation.

        this method is intended to be overridden by subclasses.

        :returns: list[str]
        :rtype: list
        """

        return []

    def _get_data(self):
        """
        gets the data required in template generation to replace in files.

        this method is intended to be overridden by subclasses.

        :rtype: dict
        """

        return {}

    def _get_config_stores(self):
        """
        gets the config store names which belong to this template.

        this method is intended to be overridden by subclasses.

        :returns: list[str]
        :rtype: list
        """

        return []

    def _finalize(self):
        """
        finalizes the template creation.

        this method is intended to be overridden by subclasses.
        """
        pass

    def _print_info(self, message):
        """
        prints the message as info.

        this method could be overridden in subclasses if
        printing is not desired for a template handler.

        :param str message: message to be printed.
        """

        print_default(message, force=True)

    @property
    def name(self):
        """
        gets the name of this template handler.

        :rtype: str
        """

        return self._name
