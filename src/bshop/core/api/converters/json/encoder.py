# -*- coding: utf-8 -*-
"""
json encoder module.
"""

from datetime import datetime, date, time

from flask.json import JSONEncoder

from bshop.core.utils.datetime.converter import to_datetime_string_utc, to_date_string, to_time_string_utc


class CoreJSONEncoder(JSONEncoder):
    """
    the default application json encoder. it extends the default flask json encoder
    to get the correct string representation for dates and times.
    """

    def default(self, o):
        """
        implement this method in a subclass such that it returns a
        serializable object for `o`, or calls the base implementation (to
        raise a `TypeError`).

        :rtype: str
        """

        if isinstance(o, datetime):
            return to_datetime_string_utc(o)
        if isinstance(o, date):
            return to_date_string(o)
        if isinstance(o, time):
            return to_time_string_utc(o)

        return JSONEncoder.default(self, o)
