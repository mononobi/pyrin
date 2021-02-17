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


def sort_by_length(items, reverse=False):
    """
    sorts the given list of strings by length of items.

    :param list[str] items: list of strings to be sorted.

    :param bool reverse: sort by descending length.
                         defaults to False if not provided.

    :rtype: list[str]
    """

    return sorted(items, key=len, reverse=reverse)


def quote(value, sign="'"):
    """
    quotes the given string value.

    :param str value: value to be quoted.
    :param str sign: quotation sign to be used.
                     defaults to single quotation if not provided.

    :rtype: str
    """

    return "{sign}{value}{sign}".format(sign=sign, value=str(value))


def union(first, second, **options):
    """
    gets the list of strings which are in both lists.

    note that it returns the value from the first list.
    by default comparison is case-insensitive.
    so if `A` is in the first list and `a` is in the second list, the
    result list will contain `A` from the first list.

    :param list[str] | set[str] | tuple[str] first: first list of strings.
    :param list[str] | set[str] | tuple[str] second: second list of strings.

    :keyword function converter: a callable to be used for case conversion of
                                 strings. it must take a single input string and
                                 return the converted value. if you want case-sensitive
                                 comparison, you could pass `str` function as converter.
                                 defaults to `lower` which results in case-insensitive
                                 comparison.

    :keyword type collection: collection type to be used for result.
                              defaults to `list` if not provided.

    :rtype: list[str] | set[str] | tuple[str]
    """

    collection = options.get('collection', list)
    converter = options.get('converter', lower)
    result = []
    second = [converter(item) for item in second]
    for item in first:
        if converter(item) in second:
            result.append(item)

    return collection(result)


def is_match(item, values, **options):
    """
    gets a value indicating that given item exists in the given list of values.

    by default comparison is case-insensitive.
    so if item is `A` and `a` is in the values list, it returns True.

    :param str item: value to be checked for matching.
    :param list[str] | set[str] | tuple[str] values: list of string values.

    :keyword function converter: a callable to be used for case conversion of
                                 strings. it must take a single input string and
                                 return the converted value. if you want case-sensitive
                                 comparison, you could pass `str` function as converter.
                                 defaults to `lower` which results in case-insensitive
                                 comparison.

    :rtype: bool
    """

    result = union([item], values, **options)
    return len(result) > 0


def get_string(value, *accepted_types):
    """
    gets the string representation of given value.

    it only converts value to string if it is of provided types.
    if no type is given, it only converts integers and floats.
    otherwise returns the same value.

    :param object value: value to be converted.

    :param type accepted_types: accepted types for conversion to string.
                                if not provided, defaults to (int, float) types.

    :returns: string or the same value.
    """

    if bool not in accepted_types and isinstance(value, bool):
        return value

    if accepted_types is None or len(accepted_types) <= 0:
        accepted_types = (int, float)

    if isinstance(value, accepted_types):
        return str(value)

    return value
