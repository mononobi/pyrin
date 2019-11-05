# -*- coding: utf-8 -*-
"""
json decoder module.
"""

from json.decoder import scanstring
from json.scanner import py_make_scanner

from flask.json import JSONDecoder

import pyrin.globalization.datetime.services as datetime_services

from pyrin.utils.datetime import DEFAULT_DATE_TIME_ISO_REGEX, \
    DEFAULT_DATE_ISO_REGEX, DEFAULT_TIME_ISO_REGEX, DEFAULT_TIME_NO_TIMEZONE_REGEX


def scanstring_extended(s, end, strict=True):
    """
    extended scan string method to be able to parse datetime strings.
    """

    s, end = scanstring(s, end, strict)
    if DEFAULT_DATE_TIME_ISO_REGEX.match(s):
        return datetime_services.to_datetime(s), end
    elif DEFAULT_DATE_ISO_REGEX.match(s):
        return datetime_services.to_date(s), end
    elif DEFAULT_TIME_ISO_REGEX.match(s) or \
            DEFAULT_TIME_NO_TIMEZONE_REGEX.match(s):
        return datetime_services.to_time(s), end
    else:
        return s, end


class CoreJSONDecoder(JSONDecoder):
    """
    the default application json decoder. it extends the default flask json decoder
    to be able to convert complex strings to their equivalent python object.
    """

    def __init__(self, *args, **kwargs):
        super(CoreJSONDecoder, self).__init__(*args, **kwargs)
        self.parse_string = scanstring_extended
        self.scan_once = py_make_scanner(self)
