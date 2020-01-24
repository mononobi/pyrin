# -*- coding: utf-8 -*-
"""
utils configuration module.
"""

from configparser import ConfigParser

from pyrin.core.context import DTO


def load(file_path):
    """
    loads configurations from given config file into a dict.

    :param str file_path: file path to be loaded.

    :raises FileNotFoundError: file not found error.

    :rtype: dict
    """

    parser = ConfigParser()
    if len(parser.read(file_path)) == 0:
        raise FileNotFoundError('Configuration file [{file}] not found.'
                                .format(file=file_path))

    sections = DTO()
    for section in parser.sections():
        values = parser.items(section)
        dic_values = DTO()
        for single_value in values:
            dic_values[single_value[0]] = eval(single_value[1])

        sections[section] = dic_values

    return sections
