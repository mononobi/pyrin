# -*- coding: utf-8 -*-
"""
template handlers package module.
"""

import os

import pyrin.utils.path as path_utils
import pyrin.application.services as application_services

from pyrin.core.structs import DTO
from pyrin.template.decorators import template_handler
from pyrin.template.enumerations import TemplateCLIHandlersEnum
from pyrin.template.handlers.base import TemplateHandlerWithInterfaceInputBase
from pyrin.template.handlers.exceptions import InvalidPackagePathError, \
    InvalidPackageClassNameError


class PackageTemplateHandlerBase(TemplateHandlerWithInterfaceInputBase):
    """
    package template handler base class.
    """

    def __init__(self, name, source):
        """
        initializes an instance of PackageTemplateHandlerBase.

        :param str name: name of the handler.
                         each handler must have a unique name.

        :param str source: source directory of template files.
        """

        self._package_path = None
        self._package_full_path = None
        self._package_name = None
        self._package_full_name = None
        self._package_title = None
        self._package_alias = None
        self._package_class_name = None
        self._application_path = application_services.get_application_main_package_path()
        self._working_directory = application_services.get_working_directory()

        super().__init__(name, source)

    def _show_interface(self, package_path=None, package_class_name=None):
        """
        shows cli prompt to get inputs from user.

        :param str package_path: the new package path. it must be a relative
                                 path inside application main package path.

        :param str package_class_name: the new package class name.

        :raises InvalidPackagePathError: invalid package path error.
        :raises InvalidPackageClassNameError: invalid package class name error.
        """

        if package_path is None:
            package_path = input('Please input the new package relative path: ')

        if package_class_name is None:
            package_class_name = input('Please input the new package class name: ')

        self._set_attributes(package_path, package_class_name)

    def _validate_inputs(self, package_path, package_class_name):
        """
        validates the inputs to be used by this handler.

        :param str package_path: the new package path. it must be a relative
                                 path inside application main package path.

        :param str package_class_name: the new package class name.

        :raises InvalidPackagePathError: invalid package path error.
        :raises InvalidPackageClassNameError: invalid package class name error.
        """

        if package_path in (None, '') or package_path.isspace() or \
                os.path.isabs(package_path):
            raise InvalidPackagePathError('New package path is invalid.')

        if package_class_name in (None, '') or package_class_name.isspace():
            raise InvalidPackageClassNameError('New package class name is invalid.')

    def _set_attributes(self, package_path, package_class_name):
        """
        sets the required attributes based on given inputs.

        :param str package_path: the new package path. it must be a relative
                                 path inside application main package path.

        :param str package_class_name: the new package class name.

        :raises InvalidPackagePathError: invalid package path error.
        :raises InvalidPackageClassNameError: invalid package class name error.
        """

        self._validate_inputs(package_path, package_class_name)

        self._package_path = package_path.rstrip(os.path.sep).rstrip(
            os.path.altsep).replace(' ', '').lower()
        self._package_full_path = os.path.abspath(os.path.join(
            self._application_path, self._package_path))
        self._package_title = ' '.join(self._package_path.split(os.path.sep)).lower().strip()
        self._package_alias = '_'.join(self._package_path.split(os.path.sep)).lower().strip()
        self._package_name = '.'.join(self._package_path.split(os.path.sep)).lower().strip()
        self._package_full_name = path_utils.get_package_name(self._package_full_path,
                                                              self._working_directory)
        self._package_class_name = package_class_name.replace(' ', '')
        self._target = self._package_full_path

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

        return DTO(PACKAGE_NAME=self._package_name,
                   PACKAGE_TITLE=self._package_title,
                   PACKAGE_ALIAS=self._package_alias,
                   PACKAGE_CLASS_NAME=self._package_class_name,
                   PACKAGE_FULL_NAME=self._package_full_name)


@template_handler()
class PackageTemplateHandler(PackageTemplateHandlerBase):
    """
    package template handler class.

    this template handler will be used to create new application packages.
    """

    def __init__(self):
        """
        initializes an instance of PackageTemplateHandler.
        """

        pyrin_path = application_services.get_pyrin_main_package_path()
        source = os.path.abspath(os.path.join(pyrin_path, 'template', 'files', 'package'))

        super().__init__(TemplateCLIHandlersEnum.PACKAGE, source)


@template_handler()
class EmptyPackageTemplateHandler(PackageTemplateHandlerBase):
    """
    empty package template handler class.

    this template handler will be used to create new empty application packages.
    """

    def __init__(self):
        """
        initializes an instance of EmptyPackageTemplateHandler.
        """

        pyrin_path = application_services.get_pyrin_main_package_path()
        source = os.path.abspath(os.path.join(pyrin_path, 'template', 'files', 'empty_package'))

        super().__init__(TemplateCLIHandlersEnum.EMPTY_PACKAGE, source)
