# -*- coding: utf-8 -*-
"""
utils configuration module.
"""

from configparser import ConfigParser

from pyrin.core.context import DTO
from pyrin.core.exceptions import CoreFileNotFoundError, CoreValueError


def load(file_path, converter=eval):
    """
    loads configurations from given config file into a dict.

    :param str file_path: file path to be loaded.

    :param callable converter: a callable to be used for converting
                               each value represented in config file.
                               the callable should accept a single argument.
                               defaults to `eval` if not provided.

    :raises CoreValueError: core value error.
    :raises CoreFileNotFoundError: core file not found error.

    :rtype: dict
    """

    if not callable(converter):
        raise CoreValueError('Input parameter [{converter}] is not callable.'
                             .format(converter=converter))

    parser = ConfigParser()
    if len(parser.read(file_path)) == 0:
        raise CoreFileNotFoundError('Configuration file [{file}] not found.'
                                    .format(file=file_path))

    sections = DTO()
    for section in parser.sections():
        values = parser.items(section)
        dic_values = DTO()
        for single_value in values:
            dic_values[single_value[0]] = converter(single_value[1])

        sections[section] = dic_values

    return sections
