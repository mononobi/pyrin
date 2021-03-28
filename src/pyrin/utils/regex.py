# -*- coding: utf-8 -*-
"""
utils regex module.
"""

import re

from pyrin.core.globals import LIST_TYPES


def matches(pattern, string, flags=0):
    """
    gets all matches of given pattern in given string in a flat tuple.

    it also removes empty matches from the result.

    :param re.Pattern | str pattern: a pattern object or a regex string.
    :param str string: value to be searched for pattern.

    :param int flags: regex flags. note that flags could only be provided
                      if given pattern is a string.

    :rtype: tuple[str]
    """

    result = re.findall(pattern, string, flags=flags)
    flat_matches = []
    for item in result:
        if isinstance(item, LIST_TYPES):
            flat_matches.extend(item)
        else:
            flat_matches.append(item)

    return tuple(item for item in flat_matches if len(item) > 0)
