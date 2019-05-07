# -*- coding: utf-8 -*-
"""
json decoder module.
"""

from json.decoder import scanstring
from json.scanner import py_make_scanner

from flask.json import JSONDecoder

from pyrin.utils.datetime.converter import DEFAULT_DATE_TIME_UTC_REGEX, \
    DEFAULT_DATE_REGEX, DEFAULT_TIME_UTC_REGEX, to_datetime_utc, to_date, to_time_utc


def scanstring_extended(s, end, strict=True):
    """
    extended scan string method to be able to parse datetime strings.
    """

    s, end = scanstring(s, end, strict)
    if DEFAULT_DATE_TIME_UTC_REGEX.match(s):
        return to_datetime_utc(s), end
    elif DEFAULT_DATE_REGEX.match(s):
        return to_date(s), end
    elif DEFAULT_TIME_UTC_REGEX.match(s):
        return to_time_utc(s), end
    else:
        return s, end


class CoreJSONDecoder(JSONDecoder):
    """
    the default application json decoder. it extends the default flask json decoder
    to be able to convert datetime strings to their equivalent python object.
    """

    def __init__(self, *args, **kwargs):
        super(CoreJSONDecoder, self).__init__(*args, **kwargs)
        self.parse_string = scanstring_extended
        self.scan_once = py_make_scanner(self)
