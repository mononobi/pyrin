# -*- coding: utf-8 -*-
"""
cli core template handlers module.
"""

import os

import pyrin.utils.path as path_utils

from pyrin.core.structs import DTO
from pyrin.template.handlers.base import TemplateHandlerWithInterfaceInputBase
from pyrin.cli.core.template.exceptions import InvalidProjectRootPathError, \
    InvalidApplicationPackageNameError, InvalidApplicationClassNameError, \
    InvalidProjectStructureTemplateHandlerType


class ProjectStructureTemplateHandlerBase(TemplateHandlerWithInterfaceInputBase):
    """
    project structure template handler base class.
    """

    def __init__(self, name, source):
        """
        initializes an instance of ProjectStructureTemplateHandlerBase.

        :param str name: name of the handler.
                         each handler must have a unique name.

        :param str source: source directory of template files.
        """

        self._next_handler = None
        self._app_package_name = None
        self._app_class_name = None
        self._project_root = None

        super().__init__(name, source)

    def set_next(self, instance):
        """
        sets the next template handler.

        :param ProjectStructureTemplateHandlerBase instance: template handler instance.

        :raises InvalidProjectStructureTemplateHandlerType: invalid project structure
                                                            template handler type.

        :rtype: ProjectStructureTemplateHandlerBase
        """

        if not isinstance(instance, ProjectStructureTemplateHandlerBase):
            raise InvalidProjectStructureTemplateHandlerType('Input parameter [{instance}] '
                                                             'is not an instance of [{base}]'
                                                             .format(instance=instance,
                                                                     base=self))

        self._next_handler = instance
        return instance

    def _show_interface(self, project_root=None,
                        app_package_name=None, app_class_name=None):
        """
        shows cli prompt to get inputs from user.

        :param str project_root: project root directory name or full path.
                                 if only a directory name is given, it will
                                 be created in current path. defaults to None
                                 if not provided and will be get from command prompt.

        :param str app_package_name: application package name.
                                     defaults to None if not provided and
                                     will be get it from command prompt.

        :param str app_class_name: application class name.
                                   defaults to None if not provided and
                                   will be get it from command prompt.

        :raises InvalidProjectRootPathError: invalid project root path error.
        :raises InvalidApplicationPackageNameError: invalid application package name error.
        :raises InvalidApplicationClassNameError: invalid application class name error.
        """

        if project_root is None:
            project_root = input('Please input the project path or directory name: ')

        if app_package_name is None:
            app_package_name = input('Please input the package name of your application: ')

        if app_class_name is None:
            app_class_name = input('Please input your application class name: ')

        self._set_attributes(project_root, app_package_name, app_class_name)

    def _validate_inputs(self, project_root, app_package_name, app_class_name):
        """
        validates the inputs to be used by this handler.

        :param str project_root: project root directory name or full path.
                                 if only a directory name is given, it will
                                 be created in current path.

        :param str app_package_name: application package name.
        :param str app_class_name: application class name.

        :raises InvalidProjectRootPathError: invalid project root path error.
        :raises InvalidApplicationPackageNameError: invalid application package name error.
        :raises InvalidApplicationClassNameError: invalid application class name error.
        """

        if project_root in (None, '') or project_root.isspace() or \
                not os.path.isabs(project_root):
            raise InvalidProjectRootPathError('Project root path is invalid.')

        if app_package_name in (None, '') or app_package_name.isspace():
            raise InvalidApplicationPackageNameError('Application package name is invalid.')

        if app_class_name in (None, '') or app_class_name.isspace():
            raise InvalidApplicationClassNameError('Application class name is invalid.')

    def _set_attributes(self, project_root, app_package_name, app_class_name):
        """
        sets the required attributes based on given inputs.

        :param str project_root: project root directory name or full path.
                                 if only a directory name is given, it will
                                 be created in current path.

        :param str app_package_name: application package name.
        :param str app_class_name: application class name.

        :raises InvalidProjectRootPathError: invalid project root path error.
        :raises InvalidApplicationPackageNameError: invalid application package name error.
        :raises InvalidApplicationClassNameError: invalid application class name error.
        """

        if project_root not in (None, '') and \
                not project_root.isspace() and not os.path.isabs(project_root):
            project_root = os.path.abspath(os.path.join('.', project_root))

        self._validate_inputs(project_root, app_package_name, app_class_name)

        self._app_class_name = app_class_name.replace(' ', '')
        self._app_package_name = app_package_name.lower().replace(' ', '')
        self._project_root = project_root.rstrip(os.path.sep).rstrip(os.path.altsep)
        self._target = self._process_target(self._project_root, self._app_package_name)

    def _process_target(self, project_root, app_package_name):
        """
        processes and gets the target value to be set for this handler's target attribute.

        it gets the project root value as target, but it could be overridden
        in subclasses to customize the target value based on given inputs.

        :param str project_root: project root absolute path.
        :param str app_package_name: application package name.
        """

        return project_root

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

        return DTO(APPLICATION_PACKAGE=self._app_package_name,
                   APPLICATION_CLASS=self._app_class_name)

    def _finalize(self):
        """
        finalizes the template creation.

        it actually calls the next handler if available, providing
        it the inputs to prevent getting them from the user again.
        """

        if self._next_handler is not None:
            return self._next_handler.create(self._project_root,
                                             self._app_package_name,
                                             self._app_class_name)


class ScriptsTemplateHandler(ProjectStructureTemplateHandlerBase):
    """
    scripts template handler class.
    """

    def __init__(self):
        """
        initializes an instance of ScriptsTemplateHandler.
        """

        pyrin_path = path_utils.get_main_package_path(self.__module__)
        source = os.path.abspath(os.path.join(pyrin_path, 'cli', 'core',
                                              'template', 'files', 'scripts'))

        super().__init__('scripts', source)


class ApplicationTemplateHandler(ProjectStructureTemplateHandlerBase):
    """
    application template handler class.
    """

    def __init__(self):
        """
        initializes an instance of ApplicationTemplateHandler.
        """

        pyrin_path = path_utils.get_main_package_path(self.__module__)
        source = os.path.abspath(os.path.join(pyrin_path, 'cli', 'core',
                                              'template', 'files', 'application'))

        super().__init__('application', source)

    def _process_target(self, project_root, app_package_name):
        """
        processes and gets the target value to be set for this handler's target attribute.

        it gets the application's main package path as target.

        :param str project_root: project root absolute path.
        :param str app_package_name: application package name.
        """

        return os.path.abspath(os.path.join(project_root, app_package_name))
