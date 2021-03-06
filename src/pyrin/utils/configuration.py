# -*- coding: utf-8 -*-
"""
utils configuration module.
"""

from configparser import ConfigParser

from pyrin.core.structs import DTO
from pyrin.utils.exceptions import InputNotCallableError, ConfigurationFileNotFoundError
from pyrin.utils.string import remove_line_break_escapes


def load(file_path, converter=eval, **options):
    """
    loads configurations from given config file into a dict.

    :param str file_path: file path to be loaded.

    :param callable converter: a callable to be used for converting
                               each value represented in config file.
                               the callable should accept a single argument.
                               defaults to `eval` if not provided.

    :keyword dict defaults: a dict containing values
                            needed for interpolation.
                            defaults to None if not provided.

    :raises InputNotCallableError: input not callable error.
    :raises ConfigurationFileNotFoundError: configuration file not found error.

    :rtype: dict
    """

    if not callable(converter):
        raise InputNotCallableError('Input parameter [{converter}] is not callable.'
                                    .format(converter=converter))

    defaults = options.get('defaults', None)
    parser = ConfigParser(defaults)
    parser.optionxform = str
    if len(parser.read(file_path)) == 0:
        raise ConfigurationFileNotFoundError('Configuration file [{file}] not found.'
                                             .format(file=file_path))

    sections = DTO()
    for section in parser.sections():
        values = parser.items(section)
        dic_values = DTO()
        for name, value in values:
            converted_value = converter(value)
            if isinstance(converted_value, str):
                converted_value = remove_line_break_escapes(converted_value)
            dic_values[name] = converted_value

        sections[section] = dic_values

    return sections
