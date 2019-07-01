# -*- coding: utf-8 -*-
"""
json encoder module.
"""

from datetime import datetime, date, time

from flask.json import JSONEncoder

from pyrin.utils import encoding
from pyrin.utils.datetime import to_datetime_string, to_date_string, \
    to_time_string


class CoreJSONEncoder(JSONEncoder):
    """
    the default application json encoder. it extends the default flask json encoder
    to get the correct string representation for other complex types.
    """

    def default(self, o):
        """
        implement this method in a subclass such that it returns a
        serializable object for `o`, or calls the base implementation (to
        raise a `TypeError`).

        :rtype: str
        """

        if isinstance(o, datetime):
            return to_datetime_string(o)
        if isinstance(o, date):
            return to_date_string(o)
        if isinstance(o, time):
            return to_time_string(o)
        if isinstance(o, bytes):
            return encoding.bytes_to_base64_string(o)

        return JSONEncoder.default(self, o)
