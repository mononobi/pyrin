# -*- coding: utf-8 -*-
"""
common utils module.
"""

import os

import pyrin.application.services as application_services

from pyrin.utils.path import assert_exists, assert_not_exists


def get_config_file_path(name):
    """
    gets the full path for given config name.

    note that the generated path is not guaranteed to be existed.

    :param str name: file name.

    :rtype: str
    """

    settings_path = application_services.get_settings_path()
    file_path = os.path.join(settings_path, name)
    return file_path


def create_config_file(name):
    """
    creates a config file in settings path.

    :param str name: file name.
    """

    file_path = get_config_file_path(name)
    command = 'touch {path}'.format(path=file_path)
    os.system(command)


def delete_config_file(name):
    """
    deletes the given config file.

    :param str name: file name.
    """

    file_path = get_config_file_path(name)
    command = 'rm -r {path}'.format(path=file_path)
    os.system(command)


def assert_config_file_existed(name):
    """
    asserts that a config file exists with given name.

    :param str name: file name.

    :raises InvalidPathError: invalid path error.
    :raises PathIsNotAbsoluteError: path is not absolute error.
    :raises PathNotExistedError: path not existed error.
    """

    file_path = get_config_file_path(name)
    assert_exists(file_path)


def assert_config_file_not_existed(name):
    """
    asserts that a config file does not exist with given name.

    :param str name: file name.

    :raises InvalidPathError: invalid path error.
    :raises PathIsNotAbsoluteError: path is not absolute error.
    :raises PathAlreadyExistedError: path already existed error.
    """

    file_path = get_config_file_path(name)
    assert_not_exists(file_path)
