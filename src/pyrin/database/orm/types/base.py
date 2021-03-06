# -*- coding: utf-8 -*-
"""
orm types base module.
"""

from abc import abstractmethod

from sqlalchemy import TypeDecorator

from pyrin.core.exceptions import CoreNotImplementedError


class CoreCustomType(TypeDecorator):
    """
    core custom type class.

    all application custom types must be subclassed from this type.
    """

    # the underlying type implementation of this custom type.
    # it must be a subclass of sqlalchemy types.
    impl = None

    @abstractmethod
    def _to_database(self, value, dialect):
        """
        converts given value to be emitted to database.

        this method must be overridden in subclasses.

        :param object value: value to be processed.
        :param Dialect dialect: the dialect in use.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: object
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def _from_database(self, value, dialect):
        """
        converts given value to python type after fetching it from database.

        :param object value: value to be processed.
        :param Dialect dialect: the dialect in use.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: object
        """

        raise CoreNotImplementedError()

    @abstractmethod
    def _coerce_to_string(self, value, dialect):
        """
        coerces the given value to string before sending to database.

        subclasses must override this method if they want to use literal params.

        :param object value: value to be processed.
        :param Dialect dialect: the dialect in use.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: str
        """

        raise CoreNotImplementedError()

    def load_dialect_impl(self, dialect):
        """
        returns a `TypeEngine` object corresponding to a dialect.

        :param Dialect dialect: the dialect in use.

        :rtype: TypeEngine
        """

        return super().load_dialect_impl(dialect)

    def compare_against_backend(self, dialect, conn_type):
        """
        returns True if this type is the same as the given database type.

        or None to allow the default implementation to compare these
        types. a return value of False means the given type does not
        match this type.

        :param Dialect dialect: the dialect in use.
        :param TypeEngine conn_type: type of the returned value from database.

        :rtype: bool
        """

        return super().compare_against_backend(dialect, conn_type)

    def process_literal_param(self, value, dialect):
        """
        receives a literal parameter value to be rendered inline within a statement.

        this method is used when the compiler renders a literal value
        without using binds, typically within DDL such as in the `server default`
        of a column or an expression within a CHECK constraint.

        the returned string will be rendered into the output string.

        :param TypeEngine value: data to operate upon. it could be `None`.
        :param Dialect dialect: the dialect in use.

        :rtype: str
        """

        if value is None:
            return value

        result = self._to_database(value, dialect)
        if result is None or isinstance(result, str):
            return result

        return self._coerce_to_string(result, dialect)

    def process_bind_param(self, value, dialect):
        """
        receives a bound parameter value to be converted.

        :param TypeEngine value: data to operate upon. it could be `None`.
        :param Dialect dialect: the dialect in use.

        :rtype: object
        """

        if value is None:
            return value

        return self._to_database(value, dialect)

    def process_result_value(self, value, dialect):
        """
        receives a result-row column value to be converted.

        :param str value: data to operate upon. it could be `None`.
        :param Dialect dialect: the dialect in use.

        :rtype: object
        """

        if value is None:
            return value

        return self._from_database(value, dialect)

    @property
    @abstractmethod
    def python_type(self):
        """
        gets the python type object expected to be returned by instances of this type.

        :raises CoreNotImplementedError: core not implemented error.

        :rtype: type
        """

        raise CoreNotImplementedError()
