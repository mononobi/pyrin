# -*- coding: utf-8 -*-
"""
orm types mixin module.
"""

import pyrin.globalization.datetime.services as datetime_services

from pyrin.database.enumerations import DialectEnum


class DateTimeMixin:
    """
    datetime mixin class.

    this is a helper class that adds ability to handle datetime
    values correctly on sqlite backend.
    on other backends, it works as default.
    """

    def literal_processor(self, dialect):
        """
        return a conversion function for processing literal values.

        that are to be rendered directly without using binds.

        this function is used when the compiler makes use of the
        `literal_binds` flag, typically used in DDL generation as well
        as in certain scenarios where backends don't accept bound parameters.

        :rtype: function
        """

        if dialect.name == DialectEnum.SQLITE:
            return self._to_database

        return None

    def bind_processor(self, dialect):
        """
        returns a conversion function for processing bind values.

        returns a callable which will receive a bind parameter value
        as the sole positional argument and will return a value to
        send to the DB-API.

        if processing is not necessary, the method should return `None`.

        :param dialect: dialect instance in use.

        :rtype: function
        """

        if dialect.name == DialectEnum.SQLITE:
            return self._to_database

        return None

    def result_processor(self, dialect, coltype):
        """
        return a conversion function for processing result row values.

        returns a callable which will receive a result row column
        value as the sole positional argument and will return a value
        to return to the user.

        if processing is not necessary, the method should return `None`.

        :param dialect: dialect instance in use.
        :param coltype: DB-API coltype argument received in `cursor.description`.

        :rtype: function
        """

        if dialect.name == DialectEnum.SQLITE:
            return self._from_database

        return None

    def _to_database(self, value):
        """
        converts given datetime to server timezone before emitting to database.

        :param datetime value: value to be processed.

        :rtype: datetime
        """

        if value is None:
            return value

        return datetime_services.convert(value, to_server=True, from_server=True)

    def _from_database(self, value):
        """
        converts given datetime to server timezone after fetching it from database.

        :param datetime value: value to be processed.

        :rtype: datetime
        """

        if value is None:
            return value

        return datetime_services.convert(value, to_server=True, from_server=True)
