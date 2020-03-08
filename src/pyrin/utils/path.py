# -*- coding: utf-8 -*-
"""
utils path module.
"""

import os
import sys
import shutil

from pyrin.utils.exceptions import PathIsNotAbsoluteError, InvalidPathError, \
    PathNotExistedError, PathAlreadyExistedError


def get_module_file_path(module_name):
    """
    gets the absolute file path of module with given name.

    :param str module_name: module name to get its file path.

    :rtype: str
    """

    return os.path.abspath(sys.modules[module_name].__file__)


def get_main_package_name(module_name):
    """
    gets the main package name from given module name.
    for example for `pyrin.database.manager` module, it
    returns `pyrin` as the main package name.

    :param str module_name: module name to get its root package name.

    :rtype str
    """

    return module_name.split('.')[0]


def get_main_package_path(module_name):
    """
    gets the absolute path of the main package of module with given name.

    :param str module_name: module name to get its main package path.

    :rtype: str
    """

    relative_module_path = module_name.replace('.', os.path.sep)
    root_package = get_main_package_name(module_name)
    absolute_module_path = get_module_file_path(module_name)
    temp_absolute_module_path = absolute_module_path.replace(relative_module_path, '*')
    excess_part = temp_absolute_module_path.split('*')[-1]
    list_path = list(temp_absolute_module_path)

    for i in range(-1, -len(list_path), -1):
        if list_path[i] == '*':
            list_path[i] = root_package
            break

    main_package_path = ''.join(list_path)
    main_package_path = main_package_path.replace('*', relative_module_path)
    main_package_path = main_package_path.replace(excess_part, '').rstrip(os.path.sep)

    return main_package_path


def get_pyrin_main_package_name():
    """
    gets the name of pyrin main package name.
    it would always be `pyrin` in normal cases.

    :rtype: str
    """

    return get_main_package_name(__name__)


def get_pyrin_main_package_path():
    """
    gets the absolute path of pyrin main package.

    :rtype: str
    """

    return get_main_package_path(__name__)


def create_directory(target):
    """
    creates a directory with given absolute target path.

    :param str target: absolute path of directory to be created.

    :raises InvalidPathError: invalid path error.
    :raises PathIsNotAbsoluteError: path is not absolute error.
    :raises PathAlreadyExistedError: path already existed error.
    """

    assert_not_exists(target)
    os.mkdir(target)


def copy_file(source, target):
    """
    copies the given source file into given target file or directory.

    note that target could also be a directory, if so,
    then the file with the source name will be generated.
    both source and target paths must be absolute.

    :param str source: source file absolute path.
    :param str target: target file or directory absolute path.

    :raises InvalidPathError: invalid path error.
    :raises PathIsNotAbsoluteError: path is not absolute error.
    :raises PathNotExistedError: path not existed error.
    """

    assert_exists(source)
    assert_absolute(target)
    shutil.copy2(source, target)


def copy_directory(source, target):
    """
    copies the given source directory contents into given target directory.

    both source and target paths must be absolute.

    :param str source: source directory absolute path.
    :param str target: target directory absolute path.

    :raises InvalidPathError: invalid path error.
    :raises PathIsNotAbsoluteError: path is not absolute error.
    :raises PathNotExistedError: path not existed error.
    """

    assert_exists(source)
    assert_absolute(target)
    shutil.copytree(source, target)


def assert_absolute(source):
    """
    asserts that given source path is absolute.

    :param str source: source path to be checked.

    :raises InvalidPathError: invalid path error.
    :raises PathIsNotAbsoluteError: path is not absolute error.
    """

    if source is None:
        raise InvalidPathError('Provided path could not be None.')

    if not os.path.isabs(source):
        raise PathIsNotAbsoluteError('Provided path [{source}] must be absolute.'
                                     .format(source=source))


def exists(source):
    """
    gets a value indicating that given source path exists on file system.

    :param str source: source path to be checked for existence.
                       it must be an absolute path.

    :raises InvalidPathError: invalid path error.
    :raises PathIsNotAbsoluteError: path is not absolute error.
    """

    assert_absolute(source)
    return os.path.exists(source)


def assert_exists(source):
    """
    asserts that given source path exists on file system.

    :param str source: source path to be checked for existence.
                       it must be an absolute path.

    :raises InvalidPathError: invalid path error.
    :raises PathIsNotAbsoluteError: path is not absolute error.
    :raises PathNotExistedError: path not existed error.
    """

    if not exists(source):
        raise PathNotExistedError('Provided path [{source}] does not exist.'
                                  .format(source=source))


def assert_not_exists(source):
    """
    asserts that given source path not exists on file system.

    :param str source: source path to be checked for not existence.
                       it must be an absolute path.

    :raises InvalidPathError: invalid path error.
    :raises PathIsNotAbsoluteError: path is not absolute error.
    :raises PathAlreadyExistedError: path already existed error.
    """

    if exists(source):
        raise PathAlreadyExistedError('Provided path [{source}] already existed.'
                                      .format(source=source))


def get_first_available_file(*paths, file_name):
    """
    gets the first path which a file with given name is resided in it.

    it returns None if the file is not available in any of given paths.

    :param str paths: paths to look for file in them.
                      all paths must be absolute.

    :param str file_name: file name with extension to look for.

    :raises InvalidPathError: invalid path error.
    :raises PathIsNotAbsoluteError: path is not absolute error.

    :returns: Union[str, None]
    :rtype: str
    """

    for single_path in paths:
        assert_absolute(single_path)
        file_path = os.path.abspath(os.path.join(single_path, file_name))
        if os.path.isfile(file_path):
            return file_path

    return None
