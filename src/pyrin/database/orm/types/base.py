# -*- coding: utf-8 -*-
"""
database orm types base module.
"""

from sqlalchemy import TypeDecorator

from pyrin.core.exceptions import CoreNotImplementedError


class CoreCustomType(TypeDecorator):
    """
    core custom type class.
    all application custom types must be subclassed from this type.
    """

    def load_dialect_impl(self, dialect):
        """
        returns a `TypeEngine` object corresponding to a dialect.

        :param Dialect dialect: the dialect in use.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: TypeEngine
        """

        raise CoreNotImplementedError()

    def process_bind_param(self, value, dialect):
        """
        receive a bound parameter value to be converted.

        :param TypeEngine value: data to operate upon. it could be `None`.
        :param Dialect dialect: the dialect in use.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: object
        """

        raise CoreNotImplementedError()

    def process_result_value(self, value, dialect):
        """
        receive a result-row column value to be converted.

        :param str value: data to operate upon. it could be `None`.
        :param Dialect dialect: the dialect in use.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: object
        """

        raise CoreNotImplementedError()

    def compare_against_backend(self, dialect, conn_type):
        """
        returns True if this type is the same as the given database type,
        or None to allow the default implementation to compare these
        types. a return value of False means the given type does not
        match this type.

        :param Dialect dialect: the dialect in use.
        :param TypeEngine conn_type: type of the returned value from database.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: bool
        """

        raise CoreNotImplementedError()
