# -*- coding: utf-8 -*-
"""
utils file module.
"""

import re
import os

import pyrin.utils.path as path_utils

from pyrin.utils.exceptions import IsNotDirectoryError


def replace_file_values_regex(source, data):
    """
    replaces the values in given file with values available in given dict.

    the replacement is done using regular expression.

    :param str source: file path to replace its values.
                       it must be an absolute path.

    :param dict[str, str] data: a dict containing all values that must be
                                replaced in given file. keys of the dict
                                must be strings representing regular
                                expressions and their values must be
                                the values that should replace them.

    :raises InvalidPathError: invalid path error.
    :raises PathIsNotAbsoluteError: path is not absolute error.
    :raises PathNotExistedError: path not existed error.
    """

    path_utils.assert_exists(source)
    if data is not None and len(data) > 0:
        with open(source, 'r') as file:
            file_data = file.read()

        for regex, value in data.items():
            file_data = re.sub(regex, value, file_data, flags=re.MULTILINE)

        with open(source, 'w') as file:
            file.write(file_data)


def replace_files_values_regex(source, data, *patterns):
    """
    replaces the values in all files with values available in given dict.

    if patterns is given, only matching files will be included.

    :param str source: directory path to process its files.
                       the operation will also include all
                       files of all subdirectories.
                       it must be an absolute path.

    :param dict[str, str] data: a dict containing all values that must be
                                replaced in given file. keys of the dict
                                must be strings representing regular
                                expressions and their values must be
                                the values that should replace them.

    :param str patterns: file name end patterns to be included
                         in replacement operation. for example
                         it could be `'.py', '.html'`.
                         all files will be included if not provided.

    :raises InvalidPathError: invalid path error.
    :raises PathIsNotAbsoluteError: path is not absolute error.
    :raises PathNotExistedError: path not existed error.
    :raises IsNotDirectoryError: is not directory error.
    """

    path_utils.assert_exists(source)
    if not os.path.isdir(source):
        raise IsNotDirectoryError('Provided path [{source}] is not a directory.'
                                  .format(source=source))

    for path, directories, files in os.walk(source, followlinks=True):
        for name in files:
            if is_match(name, *patterns):
                file_path = os.path.abspath(os.path.join(path, name))
                replace_file_values_regex(file_path, data)


def replace_file_values(source, data):
    """
    replaces the values in given file with values available in given dict.

    the file must contain dict keys to be replaced by dict values for that keys.

    :param str source: file path to replace its values.
                       it must be an absolute path.

    :param dict[str, str] data: a dict containing all values that
                                must be replaced in given file.

    :raises InvalidPathError: invalid path error.
    :raises PathIsNotAbsoluteError: path is not absolute error.
    :raises PathNotExistedError: path not existed error.
    """

    path_utils.assert_exists(source)
    if data is not None and len(data) > 0:
        with open(source, 'r') as file:
            file_data = file.read()

        file_data = file_data.format(**data)

        with open(source, 'w') as file:
            file.write(file_data)


def replace_files_values(source, data, *patterns):
    """
    replaces the values in all files with values available in given dict.

    if patterns is given, only matching files will be included.

    :param str source: directory path to process its files.
                       the operation will also include all
                       files of all subdirectories.
                       it must be an absolute path.

    :param dict[str, str] data: a dict containing all values that
                                must be replaced in given file.

    :param str patterns: file name end patterns to be included
                         in replacement operation. for example
                         it could be `'.py', '.html'`.
                         all files will be included if not provided.

    :raises InvalidPathError: invalid path error.
    :raises PathIsNotAbsoluteError: path is not absolute error.
    :raises PathNotExistedError: path not existed error.
    :raises IsNotDirectoryError: is not directory error.
    """

    path_utils.assert_exists(source)
    if not os.path.isdir(source):
        raise IsNotDirectoryError('Provided path [{source}] is not a directory.'
                                  .format(source=source))

    for path, directories, files in os.walk(source, followlinks=True):
        for name in files:
            if is_match(name, *patterns):
                file_path = os.path.abspath(os.path.join(path, name))
                replace_file_values(file_path, data)


def is_match(source, *patterns):
    """
    gets a value indicating that given file name end, matches with any of given patterns.

    :param str source: source file path.

    :param str patterns: file name end pattern. for example it could
                         be `'.py', '.html'`. it will match all file
                         names if no pattern is provided.

    :rtype: bool
    """

    if len(patterns) <= 0:
        return True

    patterns = tuple(item.lower() for item in patterns)
    return source.lower().endswith(patterns)
