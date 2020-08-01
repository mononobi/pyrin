# -*- coding: utf-8 -*-
"""
utils string module.
"""


def upper(value):
    """
    returns the uppercase copy of input string.

    :param str value: string to make uppercase.

    :rtype: str
    """

    return value.upper()


def lower(value):
    """
    returns the lowercase copy of input string.

    :param str value: string to make lowercase.

    :rtype: str
    """

    return value.lower()


def remove_line_break_escapes(value):
    """
    removes line break escapes from given value.
    it replaces `\\n` with `\n` to enable line breaks.

    :param str value: value to remove line break escapes from it.

    :rtype: str
    """

    return value.replace('\\n', '\n')


def remove_duplicate_space(value):
    """
    removes all duplicate spaces and keeps just a single space in given value.

    :param str value: value to remove duplicate spaces from it.

    :rtype: str
    """

    if value is None:
        return None

    while '  ' in value:
        value = value.replace('  ', ' ')

    return value


def interpolate(message, data):
    """
    interpolates the given message with given data.

    if data is not a dict, no interpolation will be done.

    :param str message: message to be interpolated.
    :param dict data: data to be used for interpolation.

    :rtype: str
    """

    if not isinstance(data, dict):
        return message

    return message.format(**data)
