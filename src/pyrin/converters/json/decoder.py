# -*- coding: utf-8 -*-
"""
json decoder module.
"""

from json.decoder import scanstring
from json.scanner import py_make_scanner

from flask.json import JSONDecoder

import pyrin.globalization.datetime.services as datetime_services
import pyrin.utils.unique_id as uuid_utils

from pyrin.utils.unique_id import UUID_REGEX
from pyrin.utils.datetime import DEFAULT_DATE_TIME_ISO_REGEX, \
    DEFAULT_DATE_ISO_REGEX, DEFAULT_TIME_ISO_REGEX, DEFAULT_LOCAL_NAIVE_TIME_REGEX, \
    DEFAULT_UTC_ZULU_DATE_TIME_REGEX, DEFAULT_LOCAL_NAIVE_DATE_TIME_REGEX


def scanstring_extended(s, end, strict=True):
    """
    extended scan string method to be able to parse complex strings.
    """

    s, end = scanstring(s, end, strict)
    if DEFAULT_DATE_TIME_ISO_REGEX.match(s):
        return datetime_services.to_datetime(s, to_server=False, from_server=False), end
    elif DEFAULT_DATE_ISO_REGEX.match(s):
        return datetime_services.to_date(s), end
    elif DEFAULT_TIME_ISO_REGEX.match(s) or DEFAULT_LOCAL_NAIVE_TIME_REGEX.match(s):
        return datetime_services.to_time(s), end
    elif DEFAULT_UTC_ZULU_DATE_TIME_REGEX.match(s):
        return datetime_services.to_datetime(s, to_server=False, from_server=False), end
    elif DEFAULT_LOCAL_NAIVE_DATE_TIME_REGEX.match(s):
        return datetime_services.to_datetime(s, to_server=False, from_server=False), end
    elif UUID_REGEX.match(s):
        return uuid_utils.try_get_uuid_or_value(s), end
    else:
        return s, end


class CoreJSONDecoder(JSONDecoder):
    """
    the default pyrin json decoder.

    it extends the default flask json decoder to be able to
    convert complex strings to their equivalent python object.
    """

    def __init__(self, *args, **kwargs):
        """
        initializes an instance of CoreJSONDecoder.
        """

        super().__init__(*args, **kwargs)
        self.parse_string = scanstring_extended
        self.scan_once = py_make_scanner(self)
