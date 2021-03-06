# -*- coding: utf-8 -*-
"""
orm types mixin module.
"""

from datetime import datetime

import pyrin.globalization.datetime.services as datetime_services
import pyrin.utils.datetime as datetime_utils

from pyrin.database.enumerations import DialectEnum
from pyrin.database.orm.types.base import CoreCustomType


class DateTimeMixin(CoreCustomType):
    """
    datetime mixin class.

    this is a helper class that adds ability to handle datetime
    values correctly on sqlite backend.
    on other backends, it works as default.
    """

    def _to_database(self, value, dialect):
        """
        converts given value to be emitted to database.

        :param datetime | date value: value to be processed.
        :param Dialect dialect: the dialect in use.

        :rtype: datetime
        """

        if dialect.name == DialectEnum.SQLITE:
            if not isinstance(value, datetime):
                value = datetime_utils.to_datetime_from_date(value)

            return datetime_services.convert(value, to_server=True, from_server=True)

        return value

    def _from_database(self, value, dialect):
        """
        converts given value to python type after fetching it from database.

        :param datetime | date value: value to be processed.
        :param Dialect dialect: the dialect in use.


        :rtype: datetime
        """

        if dialect.name == DialectEnum.SQLITE:
            return datetime_services.convert(value, to_server=True, from_server=True)

        return value

    def _coerce_to_string(self, value, dialect):
        """
        coerces the given value to string before sending to database.

        :param datetime | date value: value to be processed.
        :param Dialect dialect: the dialect in use.

        :rtype: str
        """

        return value

    @property
    def python_type(self):
        """
        gets the python type object expected to be returned by instances of this type.

        :rtype: type[datetime]
        """

        return datetime
