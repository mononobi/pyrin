# -*- coding: utf-8 -*-
"""
json encoder module.
"""

from datetime import datetime, date, time

from flask.json import JSONEncoder

import pyrin.globalization.datetime.services as datetime_services

from pyrin.utils import encoding


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
            return datetime_services.to_datetime_string(o)
        if isinstance(o, date):
            return datetime_services.to_date_string(o)
        if isinstance(o, time):
            return datetime_services.to_time_string(o)
        if isinstance(o, bytes):
            return encoding.bytes_to_base64_string(o)

        return JSONEncoder.default(self, o)
