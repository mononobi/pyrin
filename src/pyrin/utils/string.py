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
