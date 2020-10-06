# -*- coding: utf-8 -*-
"""
json encoder module.
"""

from datetime import datetime, date, time

from flask.json import JSONEncoder

import pyrin.globalization.datetime.services as datetime_services

from pyrin.utils import encoding
from pyrin.database.model.base import BaseEntity


class CoreJSONEncoder(JSONEncoder):
    """
    the default pyrin json encoder.

    it extends the default flask json encoder to get the
    correct string representation for other complex types.
    """

    def default(self, o):
        """
        implement this method in a subclass such that it returns a
        serializable object for `o`, or calls the base implementation (to
        raise a `TypeError`).

        this method is overridden to be able to serialize complex python
        types to json string.

        :returns: serializable object
        """

        if isinstance(o, datetime):
            return datetime_services.to_datetime_string(o, server=False)
        if isinstance(o, date):
            return datetime_services.to_date_string(o)
        if isinstance(o, time):
            return datetime_services.to_time_string(o, server=False)
        if isinstance(o, bytes):
            return encoding.bytes_to_base64_string(o)
        if isinstance(o, BaseEntity):
            return o.to_dict()

        return super().default(o)
